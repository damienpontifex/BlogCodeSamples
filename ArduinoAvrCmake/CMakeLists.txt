cmake_minimum_required(VERSION 3.0)

# specify MCU type and include toolchain file
set(AVR_MCU atmega328p)
set(CMAKE_TOOLCHAIN_FILE "${CMAKE_SOURCE_DIR}/utils/cmake-avr/generic-gcc-avr.cmake")

# Get the first usb device
execute_process(
    COMMAND ls
    COMMAND grep cu.usb
    WORKING_DIRECTORY /dev
    RESULT_VARIABLE USB_RET
    OUTPUT_VARIABLE USB_DEV
    ERROR_VARIABLE USB_ERR
    OUTPUT_STRIP_TRAILING_WHITESPACE)
if(USB_DEV)
    message(STATUS "Upload port at /dev/${USB_DEV} usb device")
    set(AVR_UPLOADTOOL_PORT /dev/${USB_DEV})
else()
    message(WARNING "Failed to find usb device: ${USB_RET} ${USB_ERR}\nEnsure usb device is currently plugged in to find the proper usb device")
endif()

set(AVR_PROGRAMMER arduino)

set(CMAKE_C_FLAGS_RELEASE "${CMAKE_C_FLAGS_RELEASE} -Wall -Os")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -Wall -Og")

project(ard)

# CPU Speed 16kHz used by delay and serial 
add_definitions(-DF_CPU=16000000)   

add_avr_executable(ard main.cpp)