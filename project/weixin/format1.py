format1 = '''

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
    $(LOAD_DB)
    ////////////////////load db//////////////////////////


	// 准备输出对象
	cJSON *array = cJSON_CreateArray();

	for (uint32_t i = 0; i < $(LOAD_DB_COUNT); i++) {
		char *result = NULL;
		uint32_t find;
        ////////////////////define//////////////////////////
        $(DEFINE_ITEM)
        ////////////////////define//////////////////////////
        
        ////////////////////load data//////////////////////////
        $(LOAD_DATA_ITEM)
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
		$(FREE_STR_ITEM)
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

'''