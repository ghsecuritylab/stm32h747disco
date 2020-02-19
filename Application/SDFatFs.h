/*
 * SDFatFs.h
 *
 *  Created on: Feb 18, 2020
 *      Author: Ericson Joseph
 */

#ifndef APPLICATION_SDFATFS_H_
#define APPLICATION_SDFATFS_H_

typedef enum {
	APPLICATION_IDLE = 0,
	APPLICATION_RUNNING,
	APPLICATION_SD_UNPLUGGED,
	APPLICATION_STATUS_CHANGED,
} FS_FileOperationsTypeDef;


void SDFatFs_Init();


#endif /* APPLICATION_SDFATFS_H_ */
