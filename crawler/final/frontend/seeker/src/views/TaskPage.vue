<template>
  <v-app>
    <v-container>
      <v-app-bar app
                 color="primary"
                 dark>
        <v-toolbar-title>Seeker Engine - 后台任务</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn @click="goToHome">主页</v-btn>
      </v-app-bar>
      <v-main>
        <v-container>
          <v-card class="mb-4"
                  outlined>
            <v-card-title>
              <span class="headline">文档统计</span>
            </v-card-title>
            <v-divider></v-divider>
            <v-card-text>
              <v-row>
                <v-col cols="6"
                       class="d-flex align-center justify-center">
                  <v-icon color="primary"
                          class="mr-2">mdi-file-document-outline</v-icon>
                  <span>原始文档数量: <strong>{{ odocsCount }}</strong></span>
                </v-col>
                <v-col cols="6"
                       class="d-flex align-center justify-center">
                  <v-icon color="primary"
                          class="mr-2">mdi-file-document-edit-outline</v-icon>
                  <span>预处理文档数量: <strong>{{ pdocsCount }}</strong></span>
                </v-col>
              </v-row>
            </v-card-text>
          </v-card>

          <v-alert v-if="alert.show"
                   :type="alert.type"
                   dismissible
                   @input="alert.show = false"
                   class="mb-4">
            {{ alert.message }}
          </v-alert>

          <v-card class="mb-4"
                  outlined>
            <v-card-title>
              <span class="headline">发布任务</span>
            </v-card-title>

            <v-divider class="my-4"></v-divider>
            <v-sheet class="pa-4">
              <v-form @submit.prevent="submitForm"
                      class="mb-4">
                <v-row>
                  <v-col cols="12">
                    <span class="headline">爬取指定数量篇最新文章</span>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field v-model="targetId"
                                  label="Target Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field v-model="count"
                                  label="Count"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-btn type="submit"
                           color="primary"
                           block
                           small>提交</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-sheet>

            <v-divider class="my-4"></v-divider>

            <v-sheet class="pa-4">
              <v-form @submit.prevent="submitCrawlOneId"
                      class="mb-4">
                <v-row>
                  <v-col cols="12">
                    <span class="headline">爬取指定 id 的文章</span>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field v-model="articleId"
                                  label="Article Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="6">
                    <v-text-field v-model="targetId"
                                  label="Target Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-btn type="submit"
                           color="primary"
                           block
                           small>提交</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-sheet>

            <v-divider class="my-4"></v-divider>

            <v-sheet class="pa-4">
              <v-form @submit.prevent="submitCrawlRangeId"
                      class="mb-4">
                <v-row>
                  <v-col cols="12">
                    <span class="headline">爬取指定范围 id 的文章</span>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field v-model="startId"
                                  label="Start Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field v-model="endId"
                                  label="End Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="4">
                    <v-text-field v-model="targetId"
                                  label="Target Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-btn type="submit"
                           color="primary"
                           block
                           small>提交</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-sheet>

            <v-divider class="my-4"></v-divider>

            <v-sheet class="pa-4">
              <v-form @submit.prevent="submitCrawlLatest100"
                      class="mb-4">
                <v-row>
                  <v-col cols="12">
                    <span class="headline">爬取最新 100 篇文章</span>
                  </v-col>
                  <v-col cols="12">
                    <v-text-field v-model="targetId"
                                  label="Target Id"
                                  type="number"
                                  dense
                                  required></v-text-field>
                  </v-col>
                  <v-col cols="12">
                    <v-btn type="submit"
                           color="primary"
                           block
                           small>提交</v-btn>
                  </v-col>
                </v-row>
              </v-form>
            </v-sheet>

            <v-divider class="my-4"></v-divider>

            <v-sheet class="pa-4">
              <v-row class="mb-4">
                <v-col cols="12">
                  <span class="headline">预处理所有文档</span>
                </v-col>
                <v-col cols="12">
                  <v-btn @click="submitPreprocessAll"
                         color="primary"
                         block
                         small>提交</v-btn>
                </v-col>
              </v-row>
            </v-sheet>

          </v-card>
        </v-container>
      </v-main>
    </v-container>
  </v-app>
</template>

<script>
import apiClient from "@/api";

export default {
  data() {
    return {
      targetId: "",
      count: "",
      articleId: "",
      startId: "",
      endId: "",
      alert: {
        show: false,
        type: "",
        message: "",
      },
      odocsCount: 0,
      pdocsCount: 0,
    };
  },

  methods: {
    async submitForm() {
      try {
        const targetId = parseInt(this.targetId, 10);
        const count = parseInt(this.count, 10);

        if (isNaN(targetId) || isNaN(count)) {
          throw new Error("Invalid input: targetId and count must be numbers.");
        }

        await apiClient.post(`/api/tasks/crawl_latest`, null, {
          params: {
            target_id: targetId,
            count: count,
          },
        });

        this.alert = {
          show: true,
          type: "success",
          message: "任务提交成功",
        };
      } catch (error) {
        console.error("Error submitting form:", error);
        this.alert = {
          show: true,
          type: "error",
          message: "任务提交失败",
        };
      }
    },
    async submitCrawlOneId() {
      try {
        const articleId = parseInt(this.articleId, 10);
        const targetId = parseInt(this.targetId, 10);

        if (isNaN(articleId) || isNaN(targetId)) {
          throw new Error("Invalid input: articleId and targetId must be numbers.");
        }

        await apiClient.post(`/api/tasks/crawl_one_id`, null, {
          params: {
            article_id: articleId,
            target_id: targetId,
          },
        });

        this.alert = {
          show: true,
          type: "success",
          message: "任务提交成功",
        };
      } catch (error) {
        console.error("Error submitting form:", error);
        this.alert = {
          show: true,
          type: "error",
          message: "任务提交失败",
        };
      }
    },
    async submitCrawlRangeId() {
      try {
        const startId = parseInt(this.startId, 10);
        const endId = parseInt(this.endId, 10);
        const targetId = parseInt(this.targetId, 10);

        if (isNaN(startId) || isNaN(endId) || isNaN(targetId)) {
          throw new Error("Invalid input: startId, endId, and targetId must be numbers.");
        }

        await apiClient.post(`/api/tasks/crawl_range_id`, null, {
          params: {
            start_id: startId,
            end_id: endId,
            target_id: targetId,
          },
        });

        this.alert = {
          show: true,
          type: "success",
          message: "任务提交成功",
        };
      } catch (error) {
        console.error("Error submitting form:", error);
        this.alert = {
          show: true,
          type: "error",
          message: "任务提交失败",
        };
      }
    },
    async submitCrawlLatest100() {
      try {
        const targetId = parseInt(this.targetId, 10);

        if (isNaN(targetId)) {
          throw new Error("Invalid input: targetId must be a number.");
        }

        await apiClient.post(`/api/tasks/crawl_latest_100`, null, {
          params: {
            target_id: targetId,
          },
        });

        this.alert = {
          show: true,
          type: "success",
          message: "任务提交成功",
        };
      } catch (error) {
        console.error("Error submitting form:", error);
        this.alert = {
          show: true,
          type: "error",
          message: "任务提交失败",
        };
      }
    },
    async submitPreprocessAll() {
      try {
        await apiClient.post(`/api/tasks/preprocess_all`);

        this.alert = {
          show: true,
          type: "success",
          message: "任务提交成功",
        };
      } catch (error) {
        console.error("Error submitting form:", error);
        this.alert = {
          show: true,
          type: "error",
          message: "任务提交失败",
        };
      }
    },
    async fetchDocCounts() {
      try {
        const odocsResponse = await apiClient.get(`/api/docs/odocs/count`);
        const pdocsResponse = await apiClient.get(`/api/docs/pdocs/count`);

        this.odocsCount = odocsResponse.data.count;
        this.pdocsCount = pdocsResponse.data.count;
        console.log("Fetched document counts:", this.odocsCount, this.pdocsCount);
      } catch (error) {
        console.error("Error fetching document counts:", error);
      }
    },
    goToHome() {
      this.$router.push({ name: "Home" });
    },
  },

  async mounted() {
    await this.fetchDocCounts();
  },
};
</script>

<style scoped></style>