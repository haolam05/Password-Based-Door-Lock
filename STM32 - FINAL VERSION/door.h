#ifndef __TRAFFIC_LIGHT_H__
#define __TRAFFIC_LIGHT_H__

#include <stdint.h>

typedef enum Door_State {S_locked, S_unlocked} State;

void Door_FSM(void);

void open_door();
void close_door();
void read_input();

#endif //__TRAFFIC_LIGHT_H__