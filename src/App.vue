<template>
   <v-app >
    <v-navigation-drawer class="hidden-md-and-up"
      fixed
      app
      left
      v-model="sideNav"
    >
    <v-card>
      
      <v-card-media
          :src=fondoNav
          height="300px"
      >
      </v-card-media>
      <v-divider></v-divider>
    </v-card>
    
     <v-list dense >
      
      <v-list-tile 
        v-for="(item) in menuItems" 
        :key=item.titulo
        :to=item.ruta
      >

        <v-list-tile-action>
          <v-icon left>{{item.icono}}</v-icon>
        </v-list-tile-action>

        <v-list-tile-content>
          <v-list-tile-title>{{item.titulo}}</v-list-tile-title>
        </v-list-tile-content>

      </v-list-tile>

     </v-list>
    

    </v-navigation-drawer>


    <v-toolbar dark class="primary ">

      <v-toolbar-side-icon class="hidden-md-and-up " @click.stop="sideNav=!sideNav"></v-toolbar-side-icon>
      
      <v-toolbar-title  >
        <router-link class="title  " to="/" tag="span" style="cursor:pointer">Nombre pagina</router-link>
      </v-toolbar-title>
      
      
      <v-spacer></v-spacer>

      <v-toolbar-items  class="hidden-sm-and-down" >

        <v-btn flat 
          v-for="item in menuItems" 
          :key="item.title"
          :to=item.ruta 
          style="cursor:pointer"
        >
          <v-icon left>{{item.icono}}</v-icon>
          {{item.titulo}}
        </v-btn>

      </v-toolbar-items>

    </v-toolbar>


    <main class="blue-grey lighten-5">
      
      <router-view/> 

    </main>
    <v-footer color="primary" app inset>
      <span class="white--text">Farmacia drogueria San Jorge &copy; 2018</span>
    </v-footer>
  </v-app>
</template>

<script lang="ts">
import { Component, Prop, Vue } from "vue-property-decorator";

@Component
export default class App extends Vue {
  public sideNav: boolean = false;
  public menuItems = [
    { icono: "fa-home", titulo: "Home", ruta: "/" },
    { icono: "fa-file-invoice", titulo: "Facturas", ruta: "/Facturas" }
  ];
  public fondoNav = require("@/assets/fondos/logo2.svg");
}
</script>

<style>
body {
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

main {
  flex: 1 0 auto;
}
h1 {
  font-size: 300%;
}
</style>
