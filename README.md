# Chess Analyzer

## Description

## Backlog

- Correct analysis order!

Case in point:
1: e4 (0.47) – c6 (0.23)
2: d4 (0.28) – d5 (0.35)
3: e5 (0.39) – Bf5 (0.26)
4: Nf3 (0.37) – e6 (0.38)
5: Nc3 (0.4) – c5 (0.29)
6: b3 (0.55) – Nc6 (-0.6)
7: Bb5 (-0.71) – Qa5 (-0.63)
8: Bxc6+ (-0.5) – bxc6 (-0.59)
9: Bd2 (-0.69) – cxd4 (-0.66)
10: Nxd5 (-0.1) – Qxd5 (-7.45)
11: Bf4 (-7.3) – Bc5 (-9.69)
12: c3 (-8.32) – dxc3 (-9.53)
...

10. Nxd5 needs to evaluate at -7.45, but currently the board state is analysed and the move is made last;
the analysis is always one turn too late.

- Analysis showing blunders, mistakes and inaccuracies
- showing lines with those blunders (show best line)
- Telegram bot accepting PGNs
- SVG generation