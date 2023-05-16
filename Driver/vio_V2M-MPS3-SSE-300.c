/******************************************************************************
 * @file     vio.c
 * @brief    Virtual I/O implementation for V2M-MPS3-SSE-300
 * @version  V1.0.0
 * @date     23. March 2020
 ******************************************************************************/
/*
 * Copyright (c) 2019-2023 Arm Limited. All rights reserved.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Licensed under the Apache License, Version 2.0 (the License); you may
 * not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an AS IS BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

/*! \page vio_V2M-MPS3-SSE-300 Physical I/O Mapping
The table below lists the physical I/O mapping of this CMSIS-Driver VIO implementation.
Virtual Resource  | Variable       | Physical Resource on V2M-MPS3-SSE-300          |
:-----------------|:---------------|:-----------------------------------------------|
vioBUTTON0        | vioSignalIn.0  | User Button PB1                                |
vioBUTTON1        | vioSignalIn.1  | User Button PB1                                |
vioLED0           | vioSignalOut.0 | User LED UL0                                   |
vioLED1           | vioSignalOut.1 | User LED UL1                                   |
vioLED2           | vioSignalOut.2 | User LED UL2                                   |
vioLED3           | vioSignalOut.3 | User LED UL3                                   |
vioLED4           | vioSignalOut.4 | User LED UL4                                   |
vioLED5           | vioSignalOut.5 | User LED UL5                                   |
vioLED6           | vioSignalOut.6 | User LED UL6                                   |
vioLED7           | vioSignalOut.7 | User LED UL7                                   |
*/

#include "cmsis_vio.h"

#include "RTE_Components.h"             // Component selection
#include CMSIS_device_header

#if !defined CMSIS_VOUT || !defined CMSIS_VIN
#include "arm_mps3_io_drv.h"
#include "device_cfg.h"
#include "device_definition.h"
#endif

// VIO input, output variables
__USED uint32_t      vioSignalIn;       // Memory for incoming signal
__USED uint32_t      vioSignalOut;      // Memory for outgoing signal

// Initialize test input, output.
void vioInit (void) {
  vioSignalIn  = 0U;
  vioSignalOut = 0U;

#if !defined CMSIS_VOUT
  // Turn off all LEDs
  arm_mps3_io_write_leds(&MPS3_IO_DEV, ARM_MPS3_IO_ACCESS_PORT, 0U, 0U);
#endif
}

// Set signal output.
void vioSetSignal (uint32_t mask, uint32_t signal) {
#if !defined CMSIS_VOUT
  uint32_t n;
#endif

  vioSignalOut &= ~mask;
  vioSignalOut |=  mask & signal;

#if !defined CMSIS_VOUT
  for (n = 0U; n < 8U; n++) {
    if (mask & (1U << n)) {
      arm_mps3_io_write_leds(&MPS3_IO_DEV, ARM_MPS3_IO_ACCESS_PIN, n, signal & (1U << n));
    }
  }
#endif
}

// Get signal input.
uint32_t vioGetSignal (uint32_t mask) {
  uint32_t signal;

#if !defined CMSIS_VIN
  vioSignalIn = arm_mps3_io_read_buttons(&MPS3_IO_DEV, ARM_MPS3_IO_ACCESS_PORT, 0);
#endif

  signal = vioSignalIn;

  return (signal & mask);
}
