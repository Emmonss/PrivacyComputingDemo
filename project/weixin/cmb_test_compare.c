/*
 * cmb_test_compare.c
 *
 *  Created on: 2024年12月17日
 *      Author: Emmons
 */
#include "hal.h"
#include "libcon.h"
#include "hal_sm3.h"
#include "hal_json.h"
#include "hal_malloc.h"
#include "hal_string.h"
#include "hal_tools.h"


// 计算 a1>b1 ? 100:0


void main(void)
{
	uint32_t pcount = HAL_GetPartyCount();
	// 两个参与方
	if (pcount != 2) {
		HAL_SetErrCode(7001);
		return;
	}
	// 获取税总方id
	char *strsz_key = NULL;
	uint32_t strsz_key_len = 0;
	uint32_t ret = HAL_GetArgsAt("SZ_KEY", 6, &strsz_key, &strsz_key_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8001);
		return;
	}

	// 获取税总方data1
	char *strsz_data1 = NULL;
	uint32_t strsz_data1_len = 0;
	ret = HAL_GetArgsAt("SZ_DATA1", 8, &strsz_data1, &strsz_data1_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8002);
		return;
	}

	// 获取税总方data2
	char *strsz_data2 = NULL;
	uint32_t strsz_data2_len = 0;
	ret = HAL_GetArgsAt("SZ_DATA2", 8, &strsz_data2, &strsz_data2_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8003);
		return;
	}

	// 获取银行方id
	char *stryh_key = NULL;
	uint32_t stryh_key_len = 0;
	ret = HAL_GetArgsAt("YH_KEY", 6, &stryh_key, &stryh_key_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8003);
		return;
	}

	char *stryh_data1 = NULL;
	uint32_t stryh_data1_len = 0;
	// 获取银行方银行账号
	ret = HAL_GetArgsAt("YH_DATA1", 8, &stryh_data1, &stryh_data1_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8004);
		return;
	}

	char *stryh_data2 = NULL;
	uint32_t stryh_data2_len = 0;
	// 获取银行方银行账号
	ret = HAL_GetArgsAt("YH_DATA2", 8, &stryh_data2, &stryh_data2_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8005);
		return;
	}

	uint32_t sz_count = (int) (hal_ReadLittleEndianInt32((void*) (strsz_key)));
	uint32_t yh_count = (int) (hal_ReadLittleEndianInt32((void*) (stryh_key)));

	// 准备输出对象
	cJSON *array = cJSON_CreateArray();

	for (uint32_t i = 0; i < sz_count; i++) {
		char *result = NULL;
		uint32_t find;

		//sz
		char* sz_id = NULL;
		char* sz_id_str = NULL;
		uint32_t sz_id_len;
		uint32_t sz_data1 = 0;
		uint32_t sz_data2 = 0;


		//yh
		char* yh_id = NULL;
		char* yh_id_str = NULL;
		uint32_t yh_id_len;
		uint32_t yh_data1 = 0;
		uint32_t yh_data2 = 0;

		//sz_id
		find = HAL_GetArrayArgsAsBytes(strsz_key, strsz_key_len, i, &sz_id, &sz_id_len);
		if (find != 0) {
			HAL_SetErrCode(9001);
			continue;
		}
		sz_id_str = hal_malloc(sz_id_len + 1);
		hal_memcpy(sz_id_str, sz_id, sz_id_len);
		sz_id_str[sz_id_len] = 0;


		//yh_id
		find = HAL_GetArrayArgsAsBytes(stryh_key, stryh_key_len, i, &yh_id, &yh_id_len);
		if (find != 0) {
			HAL_SetErrCode(9002);
			continue;
		}
		yh_id_str = hal_malloc(yh_id_len + 1);
		hal_memcpy(yh_id_str, yh_id, yh_id_len);
		yh_id_str[yh_id_len] = 0;


		//sz_data1
		find = HAL_GetArrayArgsAsUint32(strsz_data1, strsz_data1_len, i, &sz_data1);
		if (find != 0) {
			HAL_SetErrCode(9003);
			continue;
		}

		//sz_data2
		find = HAL_GetArrayArgsAsUint32(strsz_data2, strsz_data2_len, i, &sz_data2);
		if (find != 0) {
			HAL_SetErrCode(9004);
			continue;
		}

		//yz_data1
		find = HAL_GetArrayArgsAsUint32(stryh_data1, stryh_data1_len, i, &yh_data1);
		if (find != 0) {
			HAL_SetErrCode(9005);
			continue;
		}

		//yz_data2
		find = HAL_GetArrayArgsAsUint32(stryh_data2, stryh_data2_len, i, &yh_data2);
		if (find != 0) {
			HAL_SetErrCode(9006);
			continue;
		}

        //#####################################################################
        /**
        *
        *
        */
		if (hal_strcmp(sz_id_str, yh_id_str) != 0) {
			result = "-1";
		} else if(sz_data1>=yh_data1 && sz_data2>=yh_data2) {
			result = "1";
		} else if (sz_data1<yh_data1 && sz_data2>=yh_data2){
			result = "2";
		} else if (sz_data1>=yh_data1 && sz_data2<yh_data2){
			result = "3";
		} else {
			result ="4";
		}

		//add json
		cJSON *item = cJSON_CreateObject();
		cJSON_AddItemToObject(item, "sz_id", cJSON_CreateString(sz_id_str));
		cJSON_AddItemToObject(item, "result", cJSON_CreateString(result));
		cJSON_AddItemToArray(array, item);

        //#####################################################################
        //free str allocation
		hal_free(sz_id_str);
		hal_free(yh_id_str);

	}
	//json to out result
	char *out = cJSON_PrintUnformatted(array); //cJSON_Print
	uint32_t outLen = hal_strlen(out);

	// 输出结果
	HAL_SetResultInfo(0, out, outLen);
	HAL_SetResultToOutput();
	cJSON_free(array);

}



