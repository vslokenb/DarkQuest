#!/bin/bash
# Generate DY (or J/psi) events at a series of z slices with RecoE1039SimZ.C
# (copy of RecoE1039Sim.C with a z range for the vertex: args 15 and 16).
# Run from SimHits/macro after: source ../setup_mye1039.sh
#
# Usage: ./run_dy_zscan.sh [isim] [nevt] [half_width_cm] [pileup] [outdir] [z values...]
#   isim   4 = DY (default), 5 = J/psi
#   nevt   events PROCESSED per slice (default 200; fewer survive acceptance)
#   pileup true/false (default false); true needs the /pnfs pileup file
ISIM=${1:-4}
NEVT=${2:-200}
HALF=${3:-5}
PILEUP=${4:-false}
OUT=${5:-zscan_out}
shift $(( $# < 5 ? $# : 5 ))   # drop the option arguments; what is left is the z list
ZLIST=${@:-"-300 -150 0 50 100 150 200 300 400"}
PUFILE=/pnfs/e1039/persistent/users/apun/bkg_study/e1039pythiaGen_26Oct21/10_bkge1039_pythia_wshielding_100M.root
TAG=$([ "$ISIM" = 5 ] && echo jpsi || echo dy)
# "Fixed": uniform z in the slice, no material weighting (works anywhere).
# "Manual": material-aware generator; only for ranges that contain whole
# material pieces - it fails for a narrow slice inside the dump.
VTXMODE=${VTXMODE:-Fixed}

mkdir -p "$OUT"
for Z in $ZLIST; do
  ZLO=$(echo "$Z - $HALF" | bc)
  ZHI=$(echo "$Z + $HALF" | bc)
  echo "== ${TAG}: z slice ${ZLO} .. ${ZHI} cm, ${NEVT} events"
  root -b -q "RecoE1039SimZ.C($NEVT, $ISIM, 0, -300, true, true, $PILEUP, \"\", \"\", \"${TAG}_z${Z}.root\", \"$OUT/\", \"$PUFILE\", 0, \"$VTXMODE\", $ZLO, $ZHI)" \
    > "$OUT/${TAG}_z${Z}.log" 2>&1
  grep "vertex range\|SQPrimaryVertexGen::init" "$OUT/${TAG}_z${Z}.log"   # z range actually used
  ls -l "$OUT/${TAG}_z${Z}.root" | awk '{print "   ntuple size:", $5, "bytes"}'
done
