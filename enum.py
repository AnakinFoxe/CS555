'''
@author: Anakin
'''

WINDOW_TITLE        = "Digital Image Processing (CS 555)"
WINDOW_SIZE         = (1000, 740)

MAX_GRAY_LVL        = 255

OPT_01_SHRINK       = 'Shrink'
OPT_02_ZOOM_BACK    = 'Zoom Back'
OPT_03_REDUCE_GL    = 'Reduce Gray Level'
OPT_04_TRANSFORM    = 'Transform'
OPT_05_HISTO_EQ     = 'Histogram EQ'
OPT_06_HISTO_MAT    = 'Histogram Match'
OPT_07_SPATIAL_FLT  = 'Spatial Filter'
OPT_08_BIT_PLANE    = 'Bit Planes'
OPT_09_RESTORE      = 'Restoration'

CHOICE_LIST         = [OPT_01_SHRINK,
                       OPT_02_ZOOM_BACK,
                       OPT_03_REDUCE_GL,
                       OPT_04_TRANSFORM,
                       OPT_05_HISTO_EQ,
                       OPT_06_HISTO_MAT,
                       OPT_07_SPATIAL_FLT,
                       OPT_08_BIT_PLANE,
                       OPT_09_RESTORE]

ZOOM_REPLIC         = 'Replication Method'
ZOOM_NEAR_NGHR      = 'Nearest Neighbor'
ZOOM_BILINEAR       = 'Bilinear Interpolation'

REDUCE_GL_LEAST     = 'Reduce GL Least Sgn First'
REDUCE_GL_MOST      = 'Reduce GL Most Sgn First '

TRANS_LOG           = 'Log Transformation'
TRANS_POW           = 'Power Transformation'

HIST_EQ_GLOBAL      = 'Histogram EQ Global'
HIST_EQ_LOCAL       = 'Histogram EQ Local'

SP_FLT_SMOOTH       = 'Smooth Filter'
SP_FLT_MEDIAN       = 'Median Filter'
SP_FLT_LAPLACIAN    = 'Sharpening Laplacian'
SP_FLT_H_BOOST      = 'High-boosting Filter'

RESTORE_ARITHMETIC  = 'Arithmetic Mean'
RESTORE_GEOMETRIC   = 'Geometric Mean'
RESTORE_HARMONIC    = 'Harmonic Mean'
RESTORE_CONTRAHARM  = 'Contraharmonic Mean'
RESTORE_MAX         = 'Max'
RESTORE_MIN         = 'Min'
RESTORE_MIDPOINT    = 'Midpoint'
RESTORE_ALPHA_TRIM  = 'Alpha-trimmed Mean'



#DEFAULT_WIDTH       = 480
#DEFAULT_HEIGHT      = 640
#DEFAULT_WIDTH       = 464    # moon
#DEFAULT_HEIGHT      = 538    # moon

#DEFAULT_WIDTH       = 464   # EE board 1
#DEFAULT_HEIGHT      = 448   # EE board 1
DEFAULT_WIDTH       = 455   # EE board 2
DEFAULT_HEIGHT      = 440   # EE board 2

DEFAULT_WIDTH_MIN   = 60
DEFAULT_HEIGHT_MIN  = 80

DEFAULT_GRAY_LEVEL  = 4 # 4bits
DEFAULT_SIGN        = REDUCE_GL_LEAST # Least first

DEFAULT_TRANS       = TRANS_LOG
DEFAULT_C           = 2
DEFAULT_GAMMA       = 1.5

DEFAULT_HIST_EQ     = HIST_EQ_GLOBAL

DEFAULT_RESLTN_MIN  = 3

DEFAULT_LAPLACIAN   = 4
DEFAULT_K           = 2

