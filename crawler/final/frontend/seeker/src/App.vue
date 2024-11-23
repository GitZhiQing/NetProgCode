<template>
  <v-app>
    <v-container>
      <v-app-bar app
                 color="primary"
                 dark>
        <v-toolbar-title>Seeker Engine - 网络安全资讯搜索引擎</v-toolbar-title>
      </v-app-bar>
      <v-main>
        <v-container>
          <v-row justify="start">
            <v-col cols="12" md="6">
              <SearchComponent />
            </v-col>
          </v-row>
        </v-container>
      </v-main>
    </v-container>
  </v-app>
</template>

<script>
import SearchComponent from "./components/SearchComponent.vue";

export default {
  name: "App",
  components: {
    SearchComponent,
  },
  mounted() {
    document.title = "Seeker Engine";
  },
};
</script>

<style></style>