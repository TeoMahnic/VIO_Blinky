# AVH VIO Blinky example

The **Blinky** example is a simple demonstration of Python VIO module interaction with the application running on AVH model. Application VIO (LEDs, buttons) is therefore handled with Python script. Status of LEDs is printed to the terminal like `LED: 00000000`, where each digit represents one LED (e.g. `LED: 00000001` means LED0 ON). The same applies to buttons, which will be presented as `BTN: 00000000` in the terminal. 

## Operation

- In the beginning `vioLED0` blinks in 2 s interval. Upon pressing the `0` key on PC keyboard, `vioButton0` event is registered.
- Blinking rate of `vioLED0` changes and `vioLED1` also starts blinking. Event on `vioLED1` triggers an automatic event on `vioButton0` which is delayed by 5 s.
- After 5s `vioLED1` stops blinking and blinking rate of `vioLED0` has returned to 2 s interval.

# Prerequisites

- [CMSIS-Toolbox 1.5.0](https://github.com/Open-CMSIS-Pack/cmsis-toolbox/releases/tag/1.5.0) or later
- Arm Compiler 6.18 or later

# Build

1. Use the `csolution` command to create `.cprj` project files.
   ```
   csolution convert -s Blinky.csolution.yml
   ```
2. Use the `cbuild` command to create executable files.
   ```
   cbuild Blinky.Debug+AVH.cprj
   cbuild Blinky.Release+AVH.cprj
   ```

# Run
## AVH Target

Execute the following steps:
 - run the VHT model from the command line by executing:
   ```
   VHT_MPS3_Corstone_SSE-300 -f ./fvp_config.txt -V ./Python out/Blinky/AVH/Debug/Blinky.axf
   ```
- Press key `0` on PC keyboard to change LED blinking rate.
  >Note: Terminal printing LED status must have focus for input to be registered.