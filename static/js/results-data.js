/* Final retention (%), mean and sample standard deviation over three seeds.
 * Source: the manuscript's complete per-dataset results tables.
 * Dataset order: Symbol-QA, LLM-QA, Real-QA.
 * Keys follow SI, SD, replay, merged LoRA. Missing merge means shared LoRA.
 */
"use strict";
const COMPOSE_CL_RESULTS = {
  vanilla:            {mean: [1.0, 1.4, 1.3], std: [0.1, 0.0, 0.2]},
  si:                 {mean: [1.3, 1.8, 4.7], std: [0.1, 0.1, 0.2]},
  sd:                 {mean: [3.3, 2.8, 6.6], std: [0.0, 0.0, 0.1]},
  replay:             {mean: [4.2, 7.5, 12.5], std: [0.9, 2.7, 1.4]},
  merge:              {mean: [1.7, 3.0, 4.0], std: [0.1, 0.3, 0.4]},
  si_sd:              {mean: [6.9, 8.7, 14.2], std: [0.6, 0.5, 0.6]},
  si_replay:          {mean: [7.6, 15.5, 19.8], std: [0.8, 2.7, 0.9]},
  si_merge:           {mean: [1.5, 2.5, 6.5], std: [0.2, 0.0, 0.4]},
  sd_replay:          {mean: [9.0, 9.4, 9.5], std: [0.5, 1.0, 0.8]},
  sd_merge:           {mean: [11.8, 12.8, 20.2], std: [1.3, 0.8, 0.4]},
  replay_merge:       {mean: [16.6, 32.4, 48.2], std: [5.8, 8.9, 2.8]},
  si_sd_replay:       {mean: [15.4, 18.6, 15.7], std: [0.3, 0.8, 2.6]},
  si_sd_merge:        {mean: [6.8, 18.3, 31.6], std: [5.9, 0.9, 0.6]},
  si_replay_merge:    {mean: [15.7, 41.2, 54.8], std: [3.3, 9.5, 10.4]},
  sd_replay_merge:    {mean: [23.2, 33.0, 39.0], std: [4.2, 1.8, 1.9]},
  si_sd_replay_merge: {mean: [18.5, 41.8, 44.3], std: [2.8, 1.4, 8.7]}
};
