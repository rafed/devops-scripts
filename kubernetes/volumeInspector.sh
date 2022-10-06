#!/bin/bash

#
# usage: ./volumeInspector.sh <pvc-name> <namespace>
#
# creates a temporary pod that can be use to inspect the contents
# of a pvc. the pvc is mounted in the /data directory.
#

#
# get pvcs in a namespace by running:
# kubectl get pvc -n <namespace>
#

read -r -d '' config <<-EOT
{
  "kind": "Pod",
  "apiVersion": "v1",
  "spec": {
    "volumes": [
      {
        "name": "vol",
        "persistentVolumeClaim": {
          "claimName": "$1"
        }
      }
    ],
    "containers": [
      {
        "name": "inspector",
        "image": "busybox",
        "stdin": true,
        "stdinOnce": true,
        "tty": true,
        "volumeMounts": [
          {
            "mountPath": "/data",
            "name": "vol"
          }
        ]
      }
    ]
  }
}
EOT

kubectl run -it --rm --image=busybox --restart=Never --overrides="$config" -n $2 -- bash