#include "kalman.h"

void kalman_init(kalman_filter_t *kf, float process_noise, float measurement_noise, float initial_estimate, float initial_error)
{
    if(!kf) return;
    kf -> q = process_noise;
    kf -> r = measurement_noise;
    kf -> x = initial_estimate;
    kf -> p = initial_error;
    kf -> k = 0.0f;
}