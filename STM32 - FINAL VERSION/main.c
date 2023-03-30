#include "stm32f4xx.h"
#include "stm32f4_discovery.h"
#include "tm_stm32f4_servo.h"
#include "door.h"

void Delay(__IO uint32_t time);
extern __IO uint32_t TimmingDelay;

State state;
uint8_t outside_state, inside_curr_state, inside_prev_state, ras_pi_state;
TM_SERVO_t Servo1;
uint8_t servo_open_angle = 0;
uint8_t servo_close_angle = 180;

int main()
{
  // init servo pwm using TIM2_Channel 1 GPIO A5
  TM_SERVO_Init(&Servo1, TIM2, TM_PWM_Channel_1, TM_PWM_PinsPack_2);
  
  // Initialize GPIO D13 (outside button), D15 (inside button),
  // and D11 (ras pi)
  RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE); // enable GPIO A AHB clock
  GPIO_InitTypeDef GPIO_InitStruct;
  GPIO_InitStruct.GPIO_Pin = GPIO_Pin_11 | GPIO_Pin_13 | GPIO_Pin_15;
  GPIO_InitStruct.GPIO_Mode = GPIO_Mode_IN;
  GPIO_InitStruct.GPIO_Speed = GPIO_Speed_50MHz;
  GPIO_InitStruct.GPIO_OType = GPIO_OType_PP;
  GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_UP;
  GPIO_Init(GPIOD, &GPIO_InitStruct);
  
  // config Systick clock to 1000Hz
  SysTick_Config(SystemCoreClock/1000);
  
  // initialize variables
  outside_state = 0;
  inside_curr_state = 1;
  inside_prev_state = 0;
  ras_pi_state = 0;
  close_door();
  state = S_locked;
  
  while (1)
  {
    read_input();
    Door_FSM();
  }
  
  return 0;
}

void Delay(__IO uint32_t time)
{
  TimmingDelay = time;
  while(TimmingDelay !=0);
}

void Door_FSM(void)
{
  switch (state)
  {
    case S_locked:
      if ((ras_pi_state == 1) || (inside_curr_state == 1 && inside_prev_state == 0))
      {
        open_door();
      }
      break;
     
    case S_unlocked:
      if ((outside_state == 1) || (inside_curr_state == 1 && inside_prev_state == 1))
      {
        close_door();
      }
      break;
     
    default:
      break;
  }
    
}

void open_door()
{
  TM_SERVO_SetDegrees(&Servo1, servo_open_angle);
  inside_prev_state = 1;
  state = S_unlocked;
}

void close_door()
{
  TM_SERVO_SetDegrees(&Servo1, servo_close_angle);
  inside_prev_state = 0;
  state = S_locked;
}

void read_input()
{
  ras_pi_state = GPIO_ReadInputDataBit(GPIOD, GPIO_Pin_11);
  outside_state = GPIO_ReadInputDataBit(GPIOD, GPIO_Pin_13);
  inside_curr_state = GPIO_ReadInputDataBit(GPIOD, GPIO_Pin_15);
}