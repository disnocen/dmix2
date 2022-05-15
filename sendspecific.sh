#!/bin/sh

ins="$4"
outs="$5"

ins="$(echo $ins | sed 's/"/\\"/g')"
outs="$(echo $outs | sed 's/"/\\"/g')"

echo $ins $outs