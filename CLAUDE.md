# pyAltiumLib — Claude Notes

## Project
Python library for reading Altium Designer `.schlib` and `.pcblib` files and rendering components as SVG.

## Dev Environment
- Virtualenv: `~/.venv/pyaltium` — use this for all pip installs and test runs
- Source root: `src/pyaltiumlib/`

## PCB Layer IDs
Altium `.pcblib` record headers store the layer as a **single byte** (0–255).

Default layer ID assignments (from `pcblayerdefinition.py`):
| Range   | Meaning               |
|---------|-----------------------|
| 1       | Top Layer             |
| 32      | Bottom Layer          |
| 33–34   | Top/Bottom Overlay    |
| 37–38   | Top/Bottom Solder     |
| 57–72   | Mechanical 1–16       |
| 74      | Multi-Layer (vias)    |
| 81–82   | Pad/Via Holes         |

Mechanical layers 17–32 cannot use IDs 73–88 (occupied by Drill Drawing, Multi-Layer, etc.), so pyAltiumLib assigns them internal IDs 83–98 (`ID = 66 + N`). In the binary record stream, these records store **72** (Mech 16) in the common-header layer byte as a placeholder; the true layer N is encoded in the trailing bytes of the block (see "Extended Mechanical Layer Encoding" below).

## Library/LayerKindMapping/Data Format
Binary format (NOT a ParameterCollection):
```
offset  0: uint32 LE  — version block size (= 8)
offset  4: 8 bytes    — UTF-16LE version string "1.0\0"
offset 12: 4 bytes    — unknown
offset 16: uint32 LE  — entry count N
offset 20: N × 8 bytes — entries: (uint32 layer_id, uint32 kind)
```
- Old-style layer IDs (Mech 1–16): plain values 57–72 → maps to pyAltiumLib layer IDs 57–72
- New-style layer IDs (Mech 17–32): `0x04000000 + N` → maps to pyAltiumLib layer IDs 83–98 (formula: `66 + N`)
- `kind` values are defined in `PCBLayerKind` in `pcbmapping.py`

Known kind values (confirmed from `QFN50P300X300X100-17N-D.PcbLib`):
| Kind | Name                  | Confirmed |
|------|-----------------------|-----------|
| 0x01 | TopAssembly           | ✓         |
| 0x02 | BottomAssembly        | ✓         |
| 0x04 | BoardOutline          | ✓         |
| 0x0B | TopCourtyard          | ✓         |
| 0x0C | BottomCourtyard       | ✓         |
| 0x07 | TopComponentCenter    | ✓         |
| 0x08 | BottomComponentCenter | ✓         |
| 0x0D | TopDesignator         | ✓         |
| 0x0E | BottomDesignator      | ✓         |
| 0x1A | Top3DBody             | ✓         |
| 0x1B | Bottom3DBody          | ✓         |

## Extended Mechanical Layer Encoding (Mech 17–32 in binary records)
Standard binary records (Track, String, Fill, Arc) that live on Mech 17–32 store **72** in
the common-header layer byte. The true mechanical layer number N (17–32) is encoded as a
single byte in the trailing (unparsed) bytes of the block, immediately before the 3-byte
marker `\x00\x02\x01`:

```
... [parsed binary fields] ... N 00 02 01 ...
```

Confirmed from `QFN50P300X300X100-17N-D.PcbLib`: tracks on M19 have `0x13 00 02 01`,
tracks on M21 have `0x15 00 02 01`, string on M17 has `0x11 00 02 01`.

Implemented in `base.py:GenericPCBRecord._apply_extended_layer(remaining: bytes)`, called
from PcbTrack, PcbString, PcbFill, PcbArc after their fixed binary fields are read.

`PcbComponentBody` (RecordID 12) is different — it uses `V7_LAYER=MECHANICAL{N}` text
embedded in its block; see "PcbComponentBody Layer Format" below.

## PCBPad Shape Types
| Value | Name              | Notes                                     |
|-------|-------------------|-------------------------------------------|
| 1     | Round             | Uses corner_radius_percentage (100% = circle) |
| 2     | Rectangular       |                                           |
| 3     | Octagonal         | Chamfered rectangle: chamfer = min(w,h)/4 |
| 9     | Rounded Rectangle | Uses corner_radius_percentage from data   |

## PcbComponentBody Layer Format
`PcbComponentBody` (RecordID 12) does **not** use the standard 13-byte binary common header. Its block starts with binary data (`.Designator<binary>`) followed by pipe-delimited text parameters. Layer is extracted from the text: `V7_LAYER=MECHANICAL{N}`. Formula: `layer_id = 56+N` for N≤16, `66+N` for N=17–32.

## ParameterColor Byte Order
`ParameterColor(value)` interprets its integer argument as **BGR** (Altium's native format): high byte = blue, low byte = red. `to_hex()` returns `#RRGGBB`. To get a desired screen colour `#RRGGBB`, pass `(B << 16) | (G << 8) | R`. This applies to `PCBLayerKind._colors` and anywhere else a raw integer is passed to `ParameterColor`.

## Drawing Order
Layer drawing order controls the SVG `<g>` stack. Layers are added to the SVG sorted by `drawing_order` **descending**, so the highest order is added first (bottom of visual stack) and the lowest order is added last (top of visual stack).

**Lower `drawing_order` = rendered on top. Higher `drawing_order` = rendered at the bottom.**

Default drawing orders (from `LoadDefaultLayers()`): Multi-Layer=1, Top/Bottom Overlay=2, Top/Bottom Layer=6, Mechanical layers=14.

`draw_svg` sorts layers each call, so changes to `drawing_order` take effect without reloading.

## Public API — PcbLib

### `lib.get_layer(*, kind=None, name=None, id=None) → PCBLayerDefinition | None`
Look up a layer by kind name, layer name, or internal ID. Exactly one kwarg must be supplied. Returns `None` if not found, raises `ValueError` if more than one kwarg is given.

```python
lib.get_layer(kind="TopAssembly").drawing_order = 0   # render on top
lib.get_layer(name="Mechanical 21").drawing_order = 99 # render at bottom
lib.get_layer(id=87).color = ParameterColor(0x00FF00)
```

### `fp.get_records(*, kind=None, name=None, id=None) → list`
Return all records on the layer matching the given criterion. Same one-kwarg rule as `get_layer`. Returns `[]` if the layer is not found or has no records.

```python
fp.get_records(kind="TopCourtyard")   # all records on TopCourtyard
fp.get_records(name="Mechanical 21")  # same, by name
fp.get_records(id=87)                 # same, by internal ID

if not fp.get_records(kind="TopAssembly"):
    print("assembly layer is empty")
```

### `draw_svg(..., layer_kinds=None)`
`layer_kinds` accepts `PCBLayerKind` objects, raw ints, **or strings** (resolved via `PCBLayerKind.from_name`). Objects on layers with no kind assigned (`layer_type == 0`) always render regardless of the filter.

```python
fp.draw_svg(dwg, 500, 500, layer_kinds=["TopCourtyard", "TopAssembly"])
fp.draw_svg(dwg, 500, 500, layer_kinds=[PCBLayerKind(0x0B), "TopAssembly"])
```

## Known Issues / Open Questions
- `Library/LayerKindMapping` container must be opened via `self.OleObj.openstream("Library/LayerKindMapping/Data")` directly — not via `_OpenStream()` because that method sanitizes `/` in container names
