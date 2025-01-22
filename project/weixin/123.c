/Users/peizhengmeng/opt/anaconda3/envs/private_computing/bin/python /Users/peizhengmeng/code/python/PrivacyComputingDemo/project/weixin/format1_main.py 


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
	uint32_t ret = 0;
    ////////////////////load db//////////////////////////
    
    // 获取税局测试key
	char *str_sz_xid = NULL;
	uint32_t str_sz_xid_len = 0;
	ret = HAL_GetArgsAt("sz_xid", 6, &str_sz_xid, &str_sz_xid_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8001);
		return;
	}

    // 获取税局测试字段x0
	char *str_sz_x0 = NULL;
	uint32_t str_sz_x0_len = 0;
	ret = HAL_GetArgsAt("sz_x0", 5, &str_sz_x0, &str_sz_x0_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8002);
		return;
	}

    // 获取税局测试字段x1
	char *str_sz_x1 = NULL;
	uint32_t str_sz_x1_len = 0;
	ret = HAL_GetArgsAt("sz_x1", 5, &str_sz_x1, &str_sz_x1_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8003);
		return;
	}

    // 获取银行测试key
	char *str_yh_yid = NULL;
	uint32_t str_yh_yid_len = 0;
	ret = HAL_GetArgsAt("yh_yid", 6, &str_yh_yid, &str_yh_yid_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8004);
		return;
	}

    // 获取银行测试字段y0
	char *str_yh_y0 = NULL;
	uint32_t str_yh_y0_len = 0;
	ret = HAL_GetArgsAt("yh_y0", 5, &str_yh_y0, &str_yh_y0_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8005);
		return;
	}

    // 获取银行测试字段y1
	char *str_yh_y1 = NULL;
	uint32_t str_yh_y1_len = 0;
	ret = HAL_GetArgsAt("yh_y1", 5, &str_yh_y1, &str_yh_y1_len, 0);
	if (ret != 0) {
		HAL_SetErrCode(8006);
		return;
	}

    //计算数量:税局测试key
    uint32_t sz_count = (int) (hal_ReadLittleEndianInt32((void*) (str_sz_xid)));

    //计算数量:银行测试key
    uint32_t yh_count = (int) (hal_ReadLittleEndianInt32((void*) (str_yh_yid)));

    ////////////////////load db//////////////////////////


	// 准备输出对象
	cJSON *array = cJSON_CreateArray();

	for (uint32_t i = 0; i < sz_count; i++) {
		char *result = NULL;
		uint32_t find;
        ////////////////////define//////////////////////////
        
        //税局测试key-str定义
	    char* sz_xid = NULL;
	    char* sz_xid_str = NULL;
	    uint32_t sz_xid_len;
        //税局测试字段x0-int定义
        uint32_t sz_x0_data = 0;
        //税局测试字段x1-int定义
        uint32_t sz_x1_data = 0;
        //银行测试key-str定义
	    char* yh_yid = NULL;
	    char* yh_yid_str = NULL;
	    uint32_t yh_yid_len;
        //银行测试字段y0-int定义
        uint32_t yh_y0_data = 0;
        //银行测试字段y1-int定义
        uint32_t yh_y1_data = 0;
        ////////////////////define//////////////////////////
        
        ////////////////////load data//////////////////////////
        
        //sz_xid
        find = HAL_GetArrayArgsAsBytes(str_sz_xid, str_sz_xid_len, i, &sz_xid, &sz_xid_len);
        if (find != 0) {
            HAL_SetErrCode(9001);
            continue;
        }
		sz_xid_str = hal_malloc(sz_xid_len + 1);
		hal_memcpy(sz_xid_str, sz_xid, sz_xid_len);
		sz_xid_str[sz_xid_len] = 0;

        //sz_x0
		find = HAL_GetArrayArgsAsUint32(str_sz_x0, str_sz_x0_len, i, &sz_x0_data);
		if (find != 0) {
			HAL_SetErrCode(9002);
			continue;
		}

        //sz_x1
		find = HAL_GetArrayArgsAsUint32(str_sz_x1, str_sz_x1_len, i, &sz_x1_data);
		if (find != 0) {
			HAL_SetErrCode(9003);
			continue;
		}

        //yh_yid
        find = HAL_GetArrayArgsAsBytes(str_yh_yid, str_yh_yid_len, i, &yh_yid, &yh_yid_len);
        if (find != 0) {
            HAL_SetErrCode(9004);
            continue;
        }
		yh_yid_str = hal_malloc(yh_yid_len + 1);
		hal_memcpy(yh_yid_str, yh_yid, yh_yid_len);
		yh_yid_str[yh_yid_len] = 0;

        //yh_y0
		find = HAL_GetArrayArgsAsUint32(str_yh_y0, str_yh_y0_len, i, &yh_y0_data);
		if (find != 0) {
			HAL_SetErrCode(9005);
			continue;
		}

        //yh_y1
		find = HAL_GetArrayArgsAsUint32(str_yh_y1, str_yh_y1_len, i, &yh_y1_data);
		if (find != 0) {
			HAL_SetErrCode(9006);
			continue;
		}

        ////////////////////load data//////////////////////////
        
        //////////////////calculate//////////////
		// write compute fuction right here
		//////////////////calculate//////////////
        
        
        ///////////////////////////////add json result//////////////////////////////////
		//add json
		cJSON *item = cJSON_CreateObject();
		//cJSON_AddItemToObject(item, "sz_id", cJSON_CreateString(sz_id_str));
		//cJSON_AddItemToObject(item, "result", cJSON_CreateString(result));
		cJSON_AddItemToArray(array, item);
        
        ////////////////////////////free str/////////////////////////////////////
		
        //sz_xid_str  free
        hal_free(sz_xid_str);
        //yh_yid_str  free
        hal_free(yh_yid_str);
		/////////////////////////////////////////////////////////////////

	}
	//json to out result
	char *out = cJSON_PrintUnformatted(array); //cJSON_Print
	uint32_t outLen = hal_strlen(out);

	// 输出结果
	HAL_SetResultInfo(0, out, outLen);
	HAL_SetResultToOutput();
	cJSON_free(array);

}



Process finished with exit code 0
