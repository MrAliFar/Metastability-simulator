!#/bin/bash

python3 sim.py \
--sim_len 200 \
--num_reqs 50 \
--network_delay 1 \
--load AUTO \
--issue_failures 1 \
--issue_mitigations 1 \
--plot_dropped 1 \
--plot_served 1 \
--plot_retried 1