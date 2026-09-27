#include <stdio.h>
#include "kalman.h"

int main(void)
{
    kalman_filter_t kf;
    kalman_init(&kf, 0.01f, 0.5f, 0.0f, 1.0f);

    /* Simulated Noisy step response input*/
    const float noisy_inputs[8] = {0.12f, 0.98f, 0.85f, 1.05f, 0.94f, 1.02f, 0.99f, 1.01f};
    printf("Step, Measurement, EstimatedState, KalmanGain\n");
     for(uint32_t i = 0; i < 8; i++ )
     {
        float estimate = kalman_update(&kf, noisy_inputs[i]);
        printf("%u, %.4f, %.4f, %.4f\n", i, noisy_inputs[i], estimate, kf.k);
     }
     return 0;
}