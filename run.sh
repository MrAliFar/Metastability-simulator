!#/bin/bash

python3 sim.py \
--sim_len 200 \
--num_reqs 150 \
--network_delay 2 \
--load AUTO \
--issue_failures 0 \
--issue_mitigations 1 \
--plot_dropped 1 \
--plot_receive_dropped 1 \
--plot_pending_dropped 1 \
--plot_served 0 \
--plot_retried 1 \
--plot_failures 1 \
--plot_mitigations 1