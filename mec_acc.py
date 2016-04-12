import math
import numpy as np


def set_speed(speed_x,  speed_y,  speed_rot):
    robot_L = 300
    robot_W = 400
    wheel = 76.0
    factor_k = 1.0/100
    cov = 60.0/(2*math.pi)
    #print(cov)
    Ratio = 14
    coeff_arg = [[+1, -1, -1], [+1, +1, +1], [+1, +1, -1], [+1, -1, +1]]
    fl_w = (speed_x*coeff_arg[0][0]+speed_y*coeff_arg[0][1]+coeff_arg[0][2]*(robot_L+robot_W)/2*factor_k*speed_rot)/wheel
    fr_w = (speed_x*coeff_arg[1][0]+speed_y*coeff_arg[1][1]+coeff_arg[1][2]*(robot_L+robot_W)/2*factor_k*speed_rot)/wheel
    bl_w = (speed_x*coeff_arg[2][0]+speed_y*coeff_arg[2][1]+coeff_arg[2][2]*(robot_L+robot_W)/2*factor_k*speed_rot)/wheel
    br_w = (speed_x*coeff_arg[3][0]+speed_y*coeff_arg[3][1]+coeff_arg[3][2]*(robot_L+robot_W)/2*factor_k*speed_rot)/wheel
    #print(fl_w, fr_w, bl_w, br_w)
    fl_n = fl_w * cov
    fr_n = fr_w * cov
    bl_n = bl_w * cov
    br_n = br_w * cov
    PWM_FL = (50.0/6000)*14*fl_n+50
    PWM_FR = (50.0/6000)*14*fr_n+50
    PWM_BL = (50.0/6000)*14*bl_n+50
    PWM_BR = (50.0/6000)*14*br_n+50
    p1 = PWM_FL-50
    p2 = PWM_FL-50
    p3 = PWM_FL-50
    p4 = PWM_FL-50
    PWM_Max1 = max(abs(PWM_FL-50), abs(PWM_FR-50))
    PWM_Max2 = max(abs(PWM_BL-50), abs(PWM_BR-50))
    PWM_Max = max(abs(PWM_Max1), abs(PWM_Max2))
    if PWM_Max >= 48:
        PWM_FL = 48*(PWM_FL-50)/PWM_Max+50
        PWM_FR = 48*(PWM_FR-50)/PWM_Max+50
        PWM_BL = 48*(PWM_BL-50)/PWM_Max+50
        PWM_BR = 48*(PWM_BR-50)/PWM_Max+50
    real_set_fl_w = (PWM_FL - 50)/(14*50.0)*6000 / cov
    real_set_fr_w = (PWM_FR - 50)/(14*50.0)*6000 / cov
    real_set_bl_w = (PWM_BL - 50)/(14*50.0)*6000 / cov
    real_set_br_w = (PWM_BR - 50)/(14*50.0)*6000 / cov
    real_speed = [0, 0, 0]
    real_speed[0] = (coeff_arg[0][0] * real_set_fl_w + coeff_arg[1][0] * real_set_fr_w + coeff_arg[2][0] * real_set_bl_w + coeff_arg[3][0] * real_set_br_w) * wheel / 4
    real_speed[1] = (coeff_arg[0][1] * real_set_fl_w + coeff_arg[1][1] * real_set_fr_w + coeff_arg[2][1] * real_set_bl_w + coeff_arg[3][1] * real_set_br_w) * wheel / 4
    real_speed[2] = (coeff_arg[0][2] * real_set_fl_w + coeff_arg[1][2] * real_set_fr_w + coeff_arg[2][2] * real_set_bl_w + coeff_arg[3][2] * real_set_br_w) * wheel / (4 * (robot_L + robot_W)/2)/factor_k
    return (real_set_fl_w, real_set_fr_w, real_set_bl_w, real_set_br_w)


def speedCalculator(col_data, ver_data, radian_data, colSpeed_data, verSpeed_data, rotSpeed_data):
    for i in np.arange(len(col_data)-1):
        colSpeed = ((col_data[i] - col_data[i+1]) / 0.1)
        verSpeed = ((ver_data[i] - ver_data[i+1]) / 0.1)
        rotSpeed = ((radian_data[i] - radian_data[i+1]) / 0.1)
        colSpeed_data.append(colSpeed)
        verSpeed_data.append(verSpeed)
        rotSpeed_data.append(rotSpeed)

if __name__ == '__main__':
    realSpeed = set_speed(5000, 5000, 1000)
    print(realSpeed)
