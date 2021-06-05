#include <mando_xbox.h>


void main()
{
   setup_timer_3(T3_DISABLED|T3_DIV_BY_1);
   set_tris_d(0x00);
   while(1){
      output_bit(PIN_D2,0);
      delay_ms(1000);
      output_bit(PIN_D2,1);
      delay_ms(1000);
   }
   

}
