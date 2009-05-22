/* +++Date last modified: 05-Jul-1997 */

/*
**  SNIPPETS string searching functions
*/

void  init_search(const char *string);                /* Pbmsrch.C      */
char *strsearch(const char *string);                  /* Pbmsrch.C      */
void  bmh_init(const char *pattern);                  /* Bmhsrch.C      */
char *bmh_search(const char *string,                  /* Bmhsrch.C      */
                 const int stringlen);
void  bmhi_init(const char *pattern);                 /* Bhmisrch.C     */
char *bmhi_search(const char *string,                 /* Bhmisrch.C     */
                  const int stringlen);
void  bmha_init(const char *pattern);                 /* Bmhasrch.C     */
char *bmha_search(const char *string,                 /* Bmhasrch.C     */
                  const int stringlen);

/* +++Date last modified: 05-Jul-1997 */

/*
**        A Pratt-Boyer-Moore string search, written by Jerry Coffin
**  sometime or other in 1991.  Removed from original program, and
**  (incorrectly) rewritten for separate, generic use in early 1992.
**  Corrected with help from Thad Smith, late March and early
**  April 1992...hopefully it's correct this time. Revised by Bob Stout.
**
**  This is hereby placed in the Public Domain by its author.
**
**  10/21/93 rdg  Fixed bug found by Jeff Dunlop
*/

#include <stddef.h>
#include <string.h>
#include <limits.h>

static size_t table[UCHAR_MAX + 1];
static size_t len;
static char *findme;

/*
**  Call this with the string to locate to initialize the table
*/

void init_search(const char *string)
{
      size_t i;

      len = strlen(string);
      for (i = 0; i <= UCHAR_MAX; i++)                      /* rdg 10/93 */
            table[i] = len;
      for (i = 0; i < len; i++)
            table[(unsigned char)string[i]] = len - i - 1;
      findme = (char *)string;
}

/*
**  Call this with a buffer to search
*/

char *strsearch(const char *string)
{
      register size_t shift;
      register size_t pos = len - 1;
      char *here;
      size_t limit=strlen(string);

      while (pos < limit)
      {
            while( pos < limit &&
                  (shift = table[(unsigned char)string[pos]]) > 0)
            {
                  pos += shift;
            }
            if (0 == shift)
            {
                  if (0 == strncmp(findme,
                        here = (char *)&string[pos-len+1], len))
                  {
                        return(here);
                  }
                  else  pos++;
            }
      }
      return NULL;
}

#include <stdio.h>

main()
{
      char *here;
      char *find_strings[] = {"abb",  "you", "not", "it", "dad", "yoo", "hoo",
                              "oo", "oh", "xx", "xx", "x", "x", "field", "new", "row",
			      "regime", "boom", "that", "impact", "and", "zoom", "texture",
			      "magnet", "doom", "loom", "freq", "current", "phase",
			      "images",
			      "appears", "phase", "conductor", "wavez",
			      "normal", "free", "termed",
			      "provide", "for", "and", "struct", "about", "have",
			      "proper",
			      "involve",
			      "describedly",
			      "thats",
			      "spaces",
			      "circumstance",
			      "the",
			      "member",
			      "such",
			      "guide",
			      "regard",
			      "officers",
			      "implement",
			      "principalities",
			      NULL};
      char *search_strings[] = {"cabbie", "your", "It isn't here",
                                "But it is here", "hodad", "yoohoo", "yoohoo",
                                "yoohoo", "yoohoo", "yoohoo", "xx", "x", ".",
				"In recent years, the field of photonic ",
				"crystals has found new",
				"applications in the RF and microwave",
				"regime. A new type of metallic",
				"electromagnetic crystal has been",
				"developed that is having a",
				"significant impact on the field of",
				"antennas. It consists of a",
				"conductive surface, covered with a",
				"special texture which alters its",
				"electromagnetic properties. Made of solid",
				"metal, the structure",
				"conducts DC currents, but over a",
				"particular frequency range it does",
				"not conduct AC currents. It does not",
				"reverse the phase of reflected",
				"waves, and the effective image currents",
				"appear in-phase, rather than",
				"out-of-phase as they are on normal",
				"conductors. Furthermore, surface",
				"waves do not propagate, and instead",
				"radiate efficiently into free",
				"space. This new material, termed a",
				"high-impedance surface, provides",
				"a useful new ground plane for novel",
				"low-profile antennas and other",
				"electromagnetic structures.",
				"The recent protests about the Michigamua",
				"student organization have raised an",
				"important question as to the proper nature",
				"and scope of University involvement",
				"with student organizations. Accordingly",
				"the panel described in my Statement of",
				"February 25, 2000 that is considering the",
				"question of privileged space also will",
				"consider under what circumstances and in",
				"what ways the University, its",
				"administrators and faculty members should",
				"be associated with such organizations",
				"and it will recommend guiding principles",
				"in this regard. The University's",
				"Executive Officers and I will then decide",
				"whether and how to implement such",
				"principles.",
                NULL
};
      int i,j;

      for (i = 0; find_strings[i]; i++){
            for(j = 0; search_strings[j]; j++){
                init_search(find_strings[i]);
                here = strsearch(search_strings[j]);
                /*printf("\"%s\" is%s in \"%s\"", find_strings[i],
                    here ? "" : " not", search_strings[j]);
                if (here)
                    printf(" [\"%s\"]", here);
                putchar('\n');*/
        }
      }

      return 0;
}

/* +++Date last modified: 05-Jul-1997 */

/*
**  Case-sensitive Boyer-Moore-Horspool pattern match
**
**  public domain by Raymond Gardner 7/92
**
**  limitation: pattern length + string length must be less than 32767
**
**  10/21/93 rdg  Fixed bug found by Jeff Dunlop
*/
#include <limits.h>                                         /* rdg 10/93 */
#include <stddef.h>
#include <string.h>
typedef unsigned char uchar;


#define LARGE 32767

static int patlen;
static int skip[UCHAR_MAX+1];                               /* rdg 10/93 */
static int skip2;
static uchar *pat;

void bmh_init(const char *pattern)
{
          int i, lastpatchar;

          pat = (uchar *)pattern;
          patlen = strlen(pattern);
          for (i = 0; i <= UCHAR_MAX; ++i)                  /* rdg 10/93 */
                skip[i] = patlen;
          for (i = 0; i < patlen; ++i)
                skip[pat[i]] = patlen - i - 1;
          lastpatchar = pat[patlen - 1];
          skip[lastpatchar] = LARGE;
          skip2 = patlen;                 /* Horspool's fixed second shift */
          for (i = 0; i < patlen - 1; ++i)
          {
                if (pat[i] == lastpatchar)
                      skip2 = patlen - i - 1;
          }
}

char *bmh_search(const char *string, const int stringlen)
{
      int i, j;
      char *s;

      i = patlen - 1 - stringlen;
      if (i >= 0)
            return NULL;
      string += stringlen;
      for ( ;; )
      {
            while ( (i += skip[((uchar *)string)[i]]) < 0 )
                  ;                           /* mighty fast inner loop */
            if (i < (LARGE - stringlen))
                  return NULL;
            i -= LARGE;
            j = patlen - 1;
            s = (char *)string + (i - j);
            while (--j >= 0 && s[j] == pat[j])
                  ;
            if ( j < 0 )                                    /* rdg 10/93 */
                  return s;                                 /* rdg 10/93 */
            if ( (i += skip2) >= 0 )                        /* rdg 10/93 */
                  return NULL;                              /* rdg 10/93 */
      }
}
/* +++Date last modified: 05-Jul-1997 */

/*
**  Case-Insensitive Boyer-Moore-Horspool pattern match
**
**  Public Domain version by Thad Smith 7/21/1992,
**  based on a 7/92 public domain BMH version by Raymond Gardner.
**
**  This program is written in ANSI C and inherits the compilers
**  ability (or lack thereof) to support non-"C" locales by use of
**  toupper() and tolower() to perform case conversions.
**  Limitation: pattern length + string length must be less than 32767.
**
**  10/21/93 rdg  Fixed bugs found by Jeff Dunlop
*/

#include <limits.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

void bmhi_init(const char *);
char *bmhi_search(const char *, const int);
void bhmi_cleanup(void);


#define LARGE 32767             /* flag for last character match    */

static int patlen;              /* # chars in pattern               */
static int skip[UCHAR_MAX+1];   /* skip-ahead count for test chars  */
static int skip2;               /* skip-ahead after non-match with
                                ** matching final character         */
static uchar *pat = NULL;       /* uppercase copy of pattern        */

/*
** bmhi_init() is called prior to bmhi_search() to calculate the
** skip array for the given pattern.
** Error: exit(1) is called if no memory is available.
*/

void bmhi_init(const char *pattern)
{
      int i, lastpatchar;
      patlen = strlen(pattern);

      /* Make uppercase copy of pattern */

      pat = realloc ((void*)pat, patlen);
      if (!pat)
            exit(1);
      else  atexit(bhmi_cleanup);
      for (i=0; i < patlen; i++)
            pat[i] = toupper(pattern[i]);

      /* initialize skip array */

      for ( i = 0; i <= UCHAR_MAX; ++i )                    /* rdg 10/93 */
            skip[i] = patlen;
      for ( i = 0; i < patlen - 1; ++i )
      {
            skip[        pat[i] ] = patlen - i - 1;
            skip[tolower(pat[i])] = patlen - i - 1;
      }
      lastpatchar = pat[patlen - 1];
      skip[        lastpatchar ] = LARGE;
      skip[tolower(lastpatchar)] = LARGE;
      skip2 = patlen;                     /* Horspool's fixed second shift */
      for (i = 0; i < patlen - 1; ++i)
      {
            if ( pat[i] == lastpatchar )
                  skip2 = patlen - i - 1;
      }
}

char *bmhi_search(const char *string, const int stringlen)
{
      int i, j;
      char *s;

      i = patlen - 1 - stringlen;
      if (i >= 0)
            return NULL;
      string += stringlen;
      for ( ;; )
      {
            while ( (i += skip[((uchar *)string)[i]]) < 0 )
                  ;                           /* mighty fast inner loop */
            if (i < (LARGE - stringlen))
                  return NULL;
            i -= LARGE;
            j = patlen - 1;
            s = (char *)string + (i - j);
            while ( --j >= 0 && toupper(s[j]) == pat[j] )
                  ;
            if ( j < 0 )                                    /* rdg 10/93 */
                  return s;                                 /* rdg 10/93 */
            if ( (i += skip2) >= 0 )                        /* rdg 10/93 */
                  return NULL;                              /* rdg 10/93 */
      }
}

void bhmi_cleanup(void)
{
      free(pat);
}
/* +++Date last modified: 05-Jul-1997 */

/*
**  Boyer-Moore-Horspool pattern match
**  Case-insensitive with accented character translation
**
**  public domain by Raymond Gardner 7/92
**
**  limitation: pattern length + subject length must be less than 32767
**
**  10/21/93 rdg  Fixed bug found by Jeff Dunlop
*/
#include <limits.h>                                         /* rdg 10/93 */
#include <stddef.h>
#include <string.h>

#define LOWER_ACCENTED_CHARS

unsigned char lowervec[UCHAR_MAX+1] = {                     /* rdg 10/93 */
  0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15,
 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31,
 32,'!','"','#','$','%','&','\'','(',')','*','+',',','-','.','/',
'0','1','2','3','4','5','6','7','8','9',':',';','<','=','>','?',
'@','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
'p','q','r','s','t','u','v','w','x','y','z','[','\\',']','^','_',
'`','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
'p','q','r','s','t','u','v','w','x','y','z','{','|','}','~',127,
#ifdef LOWER_ACCENTED_CHARS
'c','u','e','a','a','a','a','c','e','e','e','i','i','i','a','a',
'e',145,146,'o','o','o','u','u','y','o','u',155,156,157,158,159,
'a','i','o','u','n','n',166,167,168,169,170,171,172,173,174,175,
#else
128,129,130,131,132,133,134,135,136,137,138,139,140,141,142,143,
144,145,146,147,148,149,150,151,152,153,154,155,156,157,158,159,
160,161,162,163,164,165,166,167,168,169,170,171,172,173,174,175,
#endif
176,177,178,179,180,181,182,183,184,185,186,187,188,189,190,191,
192,193,194,195,196,197,198,199,200,201,202,203,204,205,206,207,
208,209,210,211,212,213,214,215,216,217,218,219,220,221,222,223,
224,225,226,227,228,229,230,231,232,233,234,235,236,237,238,239,
240,241,242,243,244,245,246,247,248,249,250,251,252,253,254,255,
};

#define lowerc(c) lowervec[(uchar)(c)]

#define LARGE 32767

static int patlen;
static int skip[UCHAR_MAX+1];                               /* rdg 10/93 */
static int skip2;
static uchar *pat;

void bmha_init(const char *pattern)
{
      int i, j;
      pat = (uchar *)pattern;
      patlen = strlen(pattern);
      for (i = 0; i <= UCHAR_MAX; ++i)                      /* rdg 10/93 */
      {
            skip[i] = patlen;
            for (j = patlen - 1; j >= 0; --j)
            {
                  if (lowerc(i) == lowerc(pat[j]))
                        break;
            }
            if (j >= 0)
                  skip[i] = patlen - j - 1;
            if (j == patlen - 1)
                  skip[i] = LARGE;
      }
      skip2 = patlen;
      for (i = 0; i < patlen - 1; ++i)
      {
            if ( lowerc(pat[i]) == lowerc(pat[patlen - 1]) )
                  skip2 = patlen - i - 1;
      }
}

char *bmha_search(const char *string, const int stringlen)
{
      int i, j;
      char *s;

      i = patlen - 1 - stringlen;
      if (i >= 0)
            return NULL;
      string += stringlen;
      for ( ;; )
      {
            while ((i += skip[((uchar *)string)[i]]) < 0)
                  ;                           /* mighty fast inner loop */
            if (i < (LARGE - stringlen))
                  return NULL;
            i -= LARGE;
            j = patlen - 1;
            s = (char *)string + (i - j);
            while (--j >= 0 && lowerc(s[j]) == lowerc(pat[j]))
                  ;
            if ( j < 0 )                                    /* rdg 10/93 */
                  return s;                                 /* rdg 10/93 */
            if ( (i += skip2) >= 0 )                        /* rdg 10/93 */
                  return NULL;                              /* rdg 10/93 */
      }
}
