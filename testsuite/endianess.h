#include <sys/param.h>

#ifdef BYTE_ORDER
#ifdef BIG_ENDIAN
#if BYTE_ORDER == BIG_ENDIAN
#define BIG_TARGET
#endif
#endif
#endif
