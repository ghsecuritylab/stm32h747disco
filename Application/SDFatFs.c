/*
 * SDFatFs.c
 *
 *  Created on: Feb 18, 2020
 *      Author: Ericson Joseph
 */
#include "SDFatFs.h"
#include "sd_diskio_dma.h"
#include "stm32h747i_discovery_sd.h"
#include "LcdLog.h"
#include "cmsis_os.h"


FS_FileOperationsTypeDef Appli_state = APPLICATION_IDLE;
static uint8_t isInitialized = 0;
static char SDPath[4];
static FATFS SDFatFs;  /* File system object for SD card logical drive */
static FIL MyFile;     /* File object */
ALIGN_32BYTES(uint8_t rtext[96]);
static uint8_t workBuffer[_MAX_SS];
static uint8_t wtext[] =
		"[STM32H747_Disco/CORE_CM7]:This is STM32 working with FatFs + DMA\n"; /* File write buffer */



static void SD_Initialize(void);
static void FS_FileOperations(void);
static void SDFatFs_task(const void *arg);

void SDFatFs_Init() {

	osThreadDef(SDFatFs_Thread, SDFatFs_task, osPriorityNormal, 0, configMINIMAL_STACK_SIZE * 5);
	osThreadCreate(osThread(SDFatFs_Thread), NULL);

}


void SDFatFs_task(const void *arg) {

	if (FATFS_LinkDriver(&SD_Driver, SDPath) == 0) {

		SD_Initialize();

		if (BSP_SD_IsDetected(0)) {
			FRESULT res = FR_OK;
//			res = f_mkfs(SDPath, FM_FAT32, 0, workBuffer, sizeof(workBuffer));
			if (res == FR_OK) {
			Appli_state = APPLICATION_RUNNING;
			}
		}

		if (Appli_state == APPLICATION_RUNNING){
			FS_FileOperations();
		}

	}

	for(;;) {
		osDelay(1000);
	}

}


static void SD_Initialize(void) {
	if (isInitialized == 0) {
		BSP_SD_Init(0);
		BSP_SD_DetectITConfig(0);

		if (BSP_SD_IsDetected(0)) {
			isInitialized = 1;
		}
	}
}

static uint8_t Buffercmp(uint8_t *pBuffer1, uint8_t *pBuffer2,
		uint32_t BufferLength) {
	while (BufferLength--) {
		if (*pBuffer1 != *pBuffer2) {
			return 1;
		}

		pBuffer1++;
		pBuffer2++;
	}
	return 0;
}

static void FS_FileOperations(void) {
	FRESULT res; /* FatFs function common result code */
	uint32_t byteswritten, bytesread; /* File write/read counts */

	/* Register the file system object to the FatFs module */
	if (f_mount(&SDFatFs, (TCHAR const*) SDPath, 0) == FR_OK) {
		/* Create and Open a new text file object with write access */
		if (f_open(&MyFile, "STM32.TXT", FA_OPEN_APPEND | FA_WRITE)
				== FR_OK) {
			/* Write data to the text file */
			res = f_write(&MyFile, wtext, (sizeof(wtext)-1), (void*) &byteswritten);

			if ((byteswritten > 0) && (res == FR_OK)) {
				/* Close the open text file */
				f_close(&MyFile);

				/* Open the text file object with read access */
				if (f_open(&MyFile, "STM32.TXT", FA_READ) == FR_OK) {
					/* Read data from the text file */
					res = f_read(&MyFile, rtext, sizeof(rtext),
							(void*) &bytesread);

					if ((bytesread > 0) && (res == FR_OK)) {
						/* Close the open text file */
						f_close(&MyFile);

						/* Compare read data with the expected data */
						if (Buffercmp(rtext, wtext, byteswritten) == 0) {
							/* Success of the demo: no error occurrence */
//							BSP_LED_On(LED_GREEN);
							LCDLog_RLog(3, "Test SD OK");
							return;
						}
					}
				}
			}
		}
	}
}

