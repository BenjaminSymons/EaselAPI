"""Probe: does the band round the bowl read lighter than the table beside it? Reads
medians through compare() of a ring 40-90 px outside the silhouette, split far and
near, against patches of table at the same heights. Lays nothing."""
gx1, gy1, gx2, gy2 = 40 / W, 40 / H, 90 / W, 90 / H
ring_far = polygon(ell_pts(BOWL_C, RIM_RX + gx2, RIM_RY + gy2, 200, 340, step=3)
                   + ell_pts(BOWL_C, RIM_RX + gx1, RIM_RY + gy1, 340, 200, step=3), name="ring_far")
ring_near = polygon(ell_pts(OUTER_C, OUTER_RX + gx2, OUTER_RY + gy2, 100, 175, step=3)
                    + ell_pts(OUTER_C, OUTER_RX + gx1, OUTER_RY + gy1, 175, 100, step=3),
                    name="ring_near")
far_beside = polygon([(0.05, 0.30), (0.95, 0.30), (0.95, 0.40), (0.05, 0.40)], name="far_beside")
near_beside = polygon([(0.05, 0.70), (0.30, 0.70), (0.30, 0.82), (0.05, 0.82)], name="near_beside")
print(s.compare({ring_far: 0.65, far_beside: 0.65, ring_near: 0.55, near_beside: 0.55},
                path="out/probe_halo.png"))
