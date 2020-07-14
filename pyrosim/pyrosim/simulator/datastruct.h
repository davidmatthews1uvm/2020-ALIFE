#ifndef DATASTRUCT_H
#define DATASTRUCT_H

const int MAX_GROUPS = 1000;
struct Data
{
  char texturePathStr[1000];
  //simulator parameters
  int runBlind;
  float gravity;
  float dt;
  int evaluationTime;
  int speed;
  //user option
  int debug;
  int silent;
  //camera parameters
  float xyz[3];
  float hpr[3];
  int trackBody;
  int followBody;
  int collisionMatrix[MAX_GROUPS][MAX_GROUPS];
  int numCollisionGroups;
  int capture;

  int windowWidth = 100;
  int windowHeight = 100;
};

#endif
