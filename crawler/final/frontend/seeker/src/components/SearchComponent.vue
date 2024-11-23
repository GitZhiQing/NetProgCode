<template>
  <v-container width="800">
    <v-text-field v-model="query"
                  @keyup.enter="search"
                  label="关键词"
                  outlined
                  dense></v-text-field>
    <v-btn @click="search"
           color="primary"
           class="me-4">搜索</v-btn>
    <v-divider class="my-4"></v-divider>
    <v-row>
      <v-col v-for="result in results"
             :key="result.odid"
             cols="12">
        <v-card outlined>
          <v-card-title>
            <a :href="result.url"
               target="_blank"
               class="result-title">
              {{ result.title }}
            </a>
          </v-card-title>
          <v-card-subtitle>
            {{ result.first_100_words }}
          </v-card-subtitle>
          <v-card-actions>
            <v-spacer></v-spacer>
            <span class="similarity">相似度: {{ result.similarity.toFixed(3) }}</span>
          </v-card-actions>
        </v-card>
        <v-divider class="my-4"></v-divider>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiClient from "@/api";

export default {
  data() {
    return {
      query: "",
      results: [],
    };
  },
  methods: {
    async search() {
      try {
        const response = await apiClient.get(`/api/docs/`, {
          params: { query: this.query },
        });
        this.results = response.data.results;
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
  },
};
</script>

<style scoped>
.result-title {
  color: #1867c0;
  text-decoration: none;
}

.result-title:hover {
  text-decoration: underline;
}

.similarity {
  font-size: 0.75rem;
  color: gray;
}
</style>