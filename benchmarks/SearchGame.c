// This software is copyright (c) 1996-2005 by
//      John Tromp
//      Insulindeweg 908
//      1095 DX Amsterdam
//      Netherlands
// E-mail: tromp@cwi.nl
//
// This notice must not be removed.
// This software must not be sold for profit.
// You may redistribute if your distributees have the
// same rights and restrictions.

// Java Fhourstones 3.1 Transposition table logic
// (http://www.cwi.nl/~tromp/c4/fhour.html)
//
// implementation of the well-known game
// usually played on a vertical board of 7 columns by 6 rows,
// where 2 players take turns in dropping counters in a column.
// the first player to get four of his counters
// in a horizontal, vertical or diagonal row, wins the game.
// if neither player has won after 42 moves, then the game is drawn.
//
// This software is copyright (c) 1996-2005 by
//      John Tromp
//      Insulindeweg 908
//      1095 DX Amsterdam
//      Netherlands
// E-mail: tromp@cwi.nl
//
// This notice must not be removed.
// This software must not be sold for profit.
// You may redistribute if your distributees have the
// same rights and restrictions.

// Fhourstones 3.0 Board Logic
// (http://www.cwi.nl/~tromp/c4/fhour.html)
//
// implementation of the well-known game
// usually played on a vertical board of 7 columns by 6 rows,
// where 2 players take turns in dropping counters in a column.
// the first player to get four of his counters
// in a horizontal, vertical or diagonal row, wins the game.
// if neither player has won after 42 moves, then the game is drawn.
//
// This software is copyright (c) 1996-2005 by
//      John Tromp
//      Insulindeweg 908
//      1095 DX Amsterdam
//      Netherlands
// E-mail: tromp@cwi.nl
//
// This notice must not be removed.
// This software must not be sold for profit.
// You may redistribute if your distributees have the
// same rights and restrictions.

#include <stdio.h>
#include <stdlib.h>
#define WIDTH 7
#define HEIGHT 6
// bitmask corresponds to board as follows in 7x6 case:
//  .  .  .  .  .  .  .  TOP
//  5 12 19 26 33 40 47
//  4 11 18 25 32 39 46
//  3 10 17 24 31 38 45
//  2  9 16 23 30 37 44
//  1  8 15 22 29 36 43
//  0  7 14 21 28 35 42  BOTTOM
#define H1 (HEIGHT+1)
#define H2 (HEIGHT+2)
#define SIZE (HEIGHT*WIDTH)
#define SIZE1 (H1*WIDTH)
#define ALL1 (((uint64)1<<SIZE1)-(uint64)1) // assumes SIZE1 < 63
#define COL1 (((uint64)1<<H1)-(uint64)1)
#define BOTTOM (ALL1 / COL1) // has bits i*H1 set
#define TOP (BOTTOM << HEIGHT)

#include <sys/types.h>
typedef unsigned long long  uint64;
typedef long long  int64;

uint64 color[2];  // black and white bitboard
int moves[SIZE],nplies;
char height[WIDTH]; // holds bit index of lowest free square

void reset()
{
  int i;
  nplies = 0;
  color[0] = color[1] = 0;
  for (i=0; i<WIDTH; i++)
    height[i] = (char)(H1*i);
}

uint64 positioncode()
{
  return color[nplies&1] + color[0] + color[1] + BOTTOM;
// color[0] + color[1] + BOTTOM forms bitmap of heights
// so that positioncode() is a complete board encoding
}

void printMoves()
{
  int i;

  for (i=0; i<nplies; i++)
    printf("%d", 1+moves[i]);
}

// return whether newboard lacks overflowing column
int islegal(uint64 newboard)
{
  return (newboard & TOP) == 0;
}

// return whether columns col has room
int isplayable(int col)
{
  return islegal(color[nplies&1] | ((uint64)1 << height[col]));
}

// return whether newboard includes a win
int haswon(uint64 newboard)
{
  uint64 y = newboard & (newboard>>HEIGHT);
  if ((y & (y >> 2*HEIGHT)) != 0) // check \ diagonal
    return 1;
  y = newboard & (newboard>>H1);
  if ((y & (y >> 2*H1)) != 0) // check horizontal -
    return 1;
  y = newboard & (newboard>>H2); // check / diagonal
  if ((y & (y >> 2*H2)) != 0)
    return 1;
  y = newboard & (newboard>>1); // check vertical |
  return (y & (y >> 2)) != 0;
}

// return whether newboard is legal and includes a win
int islegalhaswon(uint64 newboard)
{
  return islegal(newboard) && haswon(newboard);
}

void backmove()
{
  int n;

  n = moves[--nplies];
  color[nplies&1] ^= (uint64)1<<--height[n];
}

void makemove(int n)
{
  color[nplies&1] ^= (uint64)1<<height[n]++;
  moves[nplies++] = n;
}

#define LOCKSIZE 26
#define TRANSIZE 8306069
  // should be a prime no less than about 2^{SIZE1-LOCKSIZE}
#define SYMMREC 10 // symmetry normalize first SYMMREC moves
#define UNKNOWN 0
#define LOSS 1
#define DRAWLOSS 2
#define DRAW 3
#define DRAWWIN 4
#define WIN 5
#define LOSSWIN 6

typedef struct {
  unsigned biglock:LOCKSIZE;
  unsigned bigwork:6;
  unsigned newlock:LOCKSIZE;
  unsigned newscore:3;
  unsigned bigscore:3;
} hashentry;

unsigned int htindex, lock;
hashentry *ht;

uint64 posed; // counts transtore calls

void trans_init()
{
  ht = (hashentry *)calloc(TRANSIZE, sizeof(hashentry));
}

void emptyTT()
{
  int i;

  for (i=0; i<TRANSIZE; i++) {
    ht[i] = (hashentry){0,0,0,0,0};
  }
  posed = 0;
}

void hash()
{
  uint64 htmp, htemp = positioncode();
  if (nplies < SYMMREC) { // try symmetry recognition by reversing columns
    uint64 htemp2 = 0;
    for (htmp=htemp; htmp!=0; htmp>>=H1)
      htemp2 = htemp2<<H1 | (htmp & COL1);
    if (htemp2 < htemp)
      htemp = htemp2;
  }
  lock = (unsigned int)(htemp >> (SIZE1-LOCKSIZE));
  htindex = (unsigned int)(htemp % TRANSIZE);
}

int transpose()
{
  hashentry he;
  int biglock,newlock;

  hash();
  he = ht[htindex];
  if (he.biglock == lock)
    return he.bigscore;
  if (he.newlock == lock)
    return he.newscore;
  return UNKNOWN;
}

void transtore(int x, unsigned int lock, int score, int work)
{
  hashentry he;

  posed++;
  he = ht[x];
  if (he.biglock == lock || work >= he.bigwork) {
    he.biglock = lock;
    he.bigscore = score;
    he.bigwork = work;
  } else {
    he.newlock = lock;
    he.newscore = score;
  }
  ht[x] = he;
}

void htstat()      /* some statistics on hash table performance */
{
  int total, i;
  int typecnt[8];                /* bound type stats */
  hashentry he;

  for (i=0; i<8; i++)
    typecnt[i] = 0;
  for (i=0; i<TRANSIZE; i++) {
    he = ht[i];
    if (he.biglock != 0)
      typecnt[he.bigscore]++;
    if (he.newlock != 0)
      typecnt[he.newscore]++;
  }
  for (total=0,i=LOSS; i<=WIN; i++)
    total += typecnt[i];
  if (total > 0) {
    printf("- %5.3f  < %5.3f  = %5.3f  > %5.3f  + %5.3f\n",
      typecnt[LOSS]/(double)total, typecnt[DRAWLOSS]/(double)total,
      typecnt[DRAW]/(double)total, typecnt[DRAWWIN]/(double)total,
      typecnt[WIN]/(double)total);
  }
}


#include <sys/time.h>
#include <sys/resource.h>

#define BOOKPLY 0  // full-width search up to this depth
#define REPORTPLY -1

uint64 millisecs()
{
//  struct rusage rusage;
//  getrusage(RUSAGE_SELF,&rusage);
  return 0; //rusage.ru_utime.tv_sec * 1000 + rusage.ru_utime.tv_usec / 1000;
}

int history[2][SIZE1];
uint64 nodes, msecs;

int min(int x, int y) { return x<y ? x : y; }
int max(int x, int y) { return x>y ? x : y; }

void inithistory()
{
  int side,i,h;
  for (side=0; side<2; side++)
    for (i=0; i<(WIDTH+1)/2; i++)
      for (h=0; h<H1/2; h++)
        history[side][H1*i+h] = history[side][H1*(WIDTH-1-i)+HEIGHT-1-h] =
        history[side][H1*i+HEIGHT-1-h] = history[side][H1*(WIDTH-1-i)+h] =
         4+min(3,i) + max(-1,min(3,h)-max(0,3-i)) + min(3,min(i,h)) + min(3,h);
}

int ab(int alpha, int beta)
{
  int besti,i,j,l,v,val,score,ttscore;
  int winontop,work;
  int nav,av[WIDTH];
  uint64 poscnt,newbrd,other;
  int side,otherside;
  unsigned int hashindx,hashlock;

  nodes++;
  if (nplies == SIZE-1) // one move left
    return DRAW; // by assumption, player to move can't win
  otherside = (side = nplies & 1) ^ 1;
  other = color[otherside];
  for (i = nav = 0; i < WIDTH; i++) {
    newbrd = other | ((uint64)1 << height[i]); // check opponent move
    if (!islegal(newbrd))
      continue;
    winontop = islegalhaswon(other | ((uint64)2 << height[i]));
    if (haswon(newbrd)) { // immediate threat
      if (winontop) // can't stop double threat
        return LOSS;
      nav = 0; // forced move
      av[nav++] = i;
      while (++i < WIDTH)
        if (islegalhaswon(other | ((uint64)1 << height[i])))
          return LOSS;
      break;
    }
    if (!winontop)
      av[nav++] = i;
  }
  if (nav == 0)
    return LOSS;
  if (nplies == SIZE-2) // two moves left
    return DRAW; // opponent has no win either
  if (nav == 1) {
    makemove(av[0]);
    score = LOSSWIN-ab(LOSSWIN-beta,LOSSWIN-alpha);
    backmove();
    return score;
  }
  ttscore = transpose();
  if (ttscore != UNKNOWN) {
    if (ttscore == DRAWLOSS) {
      if ((beta = DRAW) <= alpha)
        return ttscore;
    } else if (ttscore == DRAWWIN) {
      if ((alpha = DRAW) >= beta)
        return ttscore;
    } else return ttscore; // exact score
  }
  hashindx = htindex;
  hashlock = lock;
  poscnt = posed;
  besti=0;
  score = LOSS;
  for (i = 0; i < nav; i++) {
    val = history[side][(int)height[av[l = i]]];
    for (j = i+1; j < nav; j++) {
      v = history[side][(int)height[av[j]]];
      if (v > val) {
        val = v; l = j;
      }
    }
    for (j = av[l]; l>i; l--)
      av[l] = av[l-1];
    makemove(av[i] = j);
    val = LOSSWIN-ab(LOSSWIN-beta,LOSSWIN-alpha);
    backmove();
    if (val > score) {
      besti = i;
      if ((score=val) > alpha && nplies >= BOOKPLY && (alpha=val) >= beta) {
        if (score == DRAW && i < nav-1)
          score = DRAWWIN;
        if (besti > 0) {
          for (i = 0; i < besti; i++)
            history[side][(int)height[av[i]]]--; // punish bad histories
          history[side][(int)height[av[besti]]] += besti;
        }
        break;
      }
    }
  }
  if (score == LOSSWIN-ttscore) // combine < and >
    score = DRAW;
  poscnt = posed - poscnt;
  for (work=0; (poscnt>>=1) != 0; work++) ; // work=log #positions stored
  transtore(hashindx, hashlock, score, work);
  if (nplies <= REPORTPLY) {
    printMoves();
    printf("%c%d\n", "#-<=>+"[score], work);
  }
  return score;
}

int solve()
{
  int i, side = nplies & 1, otherside = side ^ 1, score;

  nodes = 0;
  msecs = 1L;
  if (haswon(color[otherside]))
      return LOSS;
  for (i = 0; i < WIDTH; i++)
    if (islegalhaswon(color[side] | ((uint64)1 << height[i])))
      return WIN;
  inithistory();
  msecs = millisecs();
  score = ab(LOSS, WIN);
  msecs = 1L + millisecs() - msecs; // prevent division by 0
  return score;
}

int main()
{
  int c, result, work;
  uint64 poscnt;
  int i = 0;
  char caratteri[] = {'1', '2', '3', '4', '5', '6', '7', '8', '3', '4', '5', '5', '6', '6'};
  //char caratteri[] = {'1', '2', '3', '5', '5', '6', '6'};

  if (sizeof(uint64) != 8) {
    printf("sizeof(uint64) == %d; please redefine.\n", sizeof(uint64));
    exit(0);
  }
  trans_init();
  puts("Fhourstones 3.1 (C)");
  printf("Boardsize = %dx%d\n",WIDTH,HEIGHT);
  printf("Using %d transposition table entries.\n", TRANSIZE);


    i = 0;
    reset();
    while (i < 14) {
      c = caratteri[i];
      if (c >= '1' && c <= '0'+WIDTH)
        makemove(c - '1');
      else if (c == '\n')
        break;
      i++;
    }
    printf("\nSolving %d-ply position after ", nplies);
    printMoves();
    puts(" . . .");

    emptyTT();
    result = solve();   // expect score << 6 | work
    poscnt = posed;
    for (work=0; (poscnt>>=1) != 0; work++) ; //work = log of #positions stored
    printf("score = %d (%c)  work = %d\n",
      result, "#-<=>+"[result], work);
    printf("%llu pos / %llu msec = %.1f Kpos/sec\n",
      nodes, msecs, (double)nodes/msecs);
    htstat();
  return 0;
}
