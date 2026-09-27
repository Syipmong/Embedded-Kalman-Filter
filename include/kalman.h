#ifndef KALMAN_H
#define KALMAN_H

#include <stdint.h>


#ifdef __cplusplus
extern "C" {
#endif

typedef struct{
    float q; /*Process Noise Covariance*/
    float r; /*Measurement Noise Covariance*/
    float x; /*Estimated State*/
    float p; /*Estimation Error Covariance*/
    float k; /*Kalman gain*/
} kalman_filter_t;

/**
 * @brief initializes the scalar discrete kalman filter state 
*/

void kalman_init(kalman_filter_t *kf, float process_noise, float measurement_noise, float initial_estimate, float initial_error);


}