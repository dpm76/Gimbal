PWR_MGM1 = 0x6b
PWR_MGM2 = 0x6c

GYRO_XOUT = 0x43
GYRO_YOUT = 0x45
GYRO_ZOUT = 0x47

ACC_XOUT = 0x3b
ACC_YOUT = 0x3d
ACC_ZOUT = 0x3f

SMPRT_DIV = 0x19

CONFIG=0x1a
GYRO_CONFIG = 0x1b
ACCEL_CONFIG = 0x1c

RESET=0b10000000
CLK_SEL_X = 1

#                  Accelerometer            |     Gyroscope
#                 F-sampling 1kHz           |
#                 Bandwidth(Hz) | Delay(ms) |  Bandwidth(Hz) | Delay (ms) | F-sampling (kHz)
#                ----------------------------------------------------------------------------
DLPF_CFG_0 = 0 #       260      |    0.0    |       256      |     0.98   |      8
DLPF_CFG_1 = 1 #       184      |    2.0    |       188      |     1.9    |      1
DLPF_CFG_2 = 2 #        94      |    3.0    |        98      |     2.8    |      1
DLPF_CFG_3 = 3 #        44      |    4.9    |        42      |     4.8    |      1
DLPF_CFG_4 = 4 #        21      |    8.5    |        20      |     8.3    |      1
DLPF_CFG_5 = 5 #        10      |   13.8    |        10      |    13.4    |      1
DLPF_CFG_6 = 6 #         5      |   19.0    |         5      |    18.6    |      1
#                ----------------------------------------------------------------------------
DLPF_CFG_7 = 7 #            RESERVED        |           RESERVED          |      8 

GFS_250 =  0
GFS_500 =  0b00001000
GFS_1000 = 0b00010000
GFS_2000 = 0b00011000

AFS_2 =  0
AFS_4 =  0b00001000
AFS_8 =  0b00010000
AFS_16 = 0b00011000
