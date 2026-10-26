# Data

Datasets are **not** committed to this repository. Download them yourself and
place them as described below. `data/raw/` is listed in `.gitignore`.

## EMOPIA 2.2

| Field | Value |
|---|---|
| Source | https://doi.org/10.5281/zenodo.5257995 |
| Project page | https://annahung31.github.io/EMOPIA |
| Version | 2.2 |
| License | Creative Commons Attribution 4.0 International (CC BY 4.0) |
| Paper | Hung et al., ISMIR 2021 |

### Setup

1. Download `EMOPIA_2.2.zip` from the Zenodo link above.
2. Unzip it into `data/raw/` and rename the folder to `emopia`.
3. Delete the `__MACOSX/` folder if the zip created one.
4. Check the download by running `python notebooks/explore_emopia.py`.

The expected layout is:

```
data/raw/emopia/
├── midis/                    # 1,071 MIDI clips (used in this project)
├── label.csv                 # clip ID, quadrant (4Q), annotator
├── key_mode_tempo.csv        # key, mode and tempo for each clip
├── metadata_by_song.csv      # clips grouped by song
├── timestamps.json           # clip start/end times in the original songs
├── corpus/                   # not used (see notes)
├── CP_events/                # not used (generation-model format)
├── REMI_events/              # not used (generation-model format)
├── metadata/                 # not used (YouTube metadata)
├── songs_lists/              # not used (YouTube URLs)
├── tagging_lists/            # not used (raw annotations)
└── scripts/                  # authors' helper scripts
```

### File naming

Files are named `Q{quadrant}_{youtube_id}_{segment}.mid`, for example
`Q1_0vLPYiPN7qY_2.mid`.

| Part | Meaning |
|---|---|
| `quadrant` | Emotion quadrant in the valence–arousal plane |
| `youtube_id` | Identifies the song; used for song-level grouping |
| `segment` | Position of the clip within the song |

| Quadrant | Valence | Arousal | Clips found |
|---|---|---|---|
| Q1 | High | High | 246 |
| Q2 | Low | High | 263 |
| Q3 | Low | Low | 253 |
| Q4 | High | Low | 309 |
| **Total** | | | **1,071** |

### Sanity checks (2026-10-26)

Produced by `notebooks/explore_emopia.py`.

| Check | Result |
|---|---|
| MIDI files in `midis/` | 1,071 |
| Unique songs | 387 |
| Rows in `label.csv` | 1,078 |
| MIDI files with a matching label | 1,071 |
| Labels without a MIDI file | 7 (the clips removed in v2.2) |
| MIDI files without a label | 0 |
| Filename quadrant differs from `label.csv` | 0 |
| Songs with clips in more than one quadrant | 72 |

### Notes

- **Clip counts differ across sources.** The paper reports 1,087 clips, the
  Zenodo notes report 1,078, and v2.2 removed 7 clips added by mistake,
  leaving 1,071. We use these 1,071 clips.
- **We use `midis/`, not `corpus/`.** `corpus/` contains only 1,052 clips
  because some were lost during the authors' preprocessing for generation.
- **MIDI files were transcribed automatically from audio** (GiantMIDI), so
  they may contain wrong or extra notes.
- **Emotion is labelled per clip, not per song.** 72 songs have clips in more
  than one quadrant. Train/test splits must still be grouped by song
  (`youtube_id`) to avoid data leakage.
- The dataset's own README names the files `.mp3`; the files in `midis/` are
  `.mid`.

### Citation

```bibtex
@inproceedings{EMOPIA,
  author    = {Hung, Hsiao-Tzu and Ching, Joann and Doh, Seungheon and
               Kim, Nabin and Nam, Juhan and Yang, Yi-Hsuan},
  title     = {{EMOPIA}: A Multi-Modal Pop Piano Dataset For Emotion
               Recognition and Emotion-based Music Generation},
  booktitle = {Proc. Int. Society for Music Information Retrieval Conf.},
  year      = {2021}
}
```