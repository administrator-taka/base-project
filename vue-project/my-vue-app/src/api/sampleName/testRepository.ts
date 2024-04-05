import { apiClient, djangoApiClient } from "@/api/sampleName/index";
import { testRequest } from "@/api/interface/request/testRequest";
import { testResponse } from "@/api/interface/response/testResponse";
import { AxiosResponse } from "axios";

export default {
  async testApi(params: testRequest): Promise<testResponse> {
    return await apiClient
      .post("/test/db", params, {
        headers: { "Content-Type": "application/json" },
      })
      .then((res: AxiosResponse<testResponse>) => {
        return res.data;
      });
  },

  async testDjangoApi(params: testRequest): Promise<testResponse> {
    console.log(params)
    return await djangoApiClient
      .post("/", null, {
        headers: { "Content-Type": "application/json" },
      })
      .then((res: AxiosResponse<testResponse>) => {
        return res.data;
      });
  },
};
