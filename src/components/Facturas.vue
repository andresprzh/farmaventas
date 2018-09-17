<template>
  <v-container grid-list-md>
    
    <h1 class="font-weight-black font-italic text-xs-center" >Titulo</h1>
    <!-- INPUTS FORMULARIO -->
      
    <v-form ref="form"  :v-model="valid" >
      <v-layout row wrap>
        <v-flex 
        xs12
        v-for="(card,index) in ent"
        :key="card.id"
        > 
         <v-menu v-if="card.tipo==='fecha'"
            lazy
            ref="menu"
            :close-on-content-click="false"
            v-model="card.menu"
            :nudge-right="40"
            :return-value.sync="card.dato"
            transition="scale-transition"
            offset-y
            full-width
            max-width="290px"
            min-width="290px"  
          >
            <v-text-field
              slot="activator"
              :v-model="card.dato"
              :label=card.titulo
              prepend-icon="fa-calendar-alt"
              readonly
              :value="card.dato"
              :error-messages="errors.collect(card.id)"
              v-validate="card.validacion"
              :data-vv-name=card.id
              @input="validar()"              
            ></v-text-field>
            <v-date-picker
              v-model="card.dato"
              no-title
              scrollable
              
            >
              <v-spacer></v-spacer>
              <v-btn flat color="primary" @click="validar();card.menu = false">Cancel</v-btn>
              
              <v-btn flat color="primary" @click="fecha($refs.menu[index],card.dato);setfecha();">OK</v-btn>
              
            </v-date-picker>
          </v-menu>

          <v-select v-else-if="card.tipo==='select'" v-show="mostrarfac"
            ref="menu"
            v-validate="card.validacion"
            :items="card.items"
            v-model="card.dato"
            :error-messages="errors.collect(card.id)"
            :label="card.titulo"
            :data-vv-name=card.id
            @change="validar();getitems();"
            required
          ></v-select>
        </v-flex>
      </v-layout>
    </v-form> 

    
    <v-layout row wrap>
      <v-flex xs12 v-show="mostrart" >
      <!-- <v-flex xs12  > -->
        <v-tabs
          centered
          v-model="tabla"
          
          color="green"
          dark
          icons-and-text
        >
          <v-tabs-slider color="black"></v-tabs-slider>

          <v-tab href="#encontrados">
            Items encontrados
            <v-icon>fa-check-circle</v-icon>
          </v-tab>

          <v-tab href="#noencontrados">
            Items no encontrados
            <v-icon>fa-times-circle</v-icon>
          </v-tab>

        </v-tabs> 
        
         <!-- DATATABLE ITEMS ENCONTRADOS-->
        <v-card v-if="tabla=='encontrados'" >
          <v-card-title class="justify-center">
            <span class="secondary--text text-xs-center" style="font-size:200%;">Items encontrados factura {{ factura }}</span><br>
          </v-card-title>
          <v-data-table
            :headers="headers"
            :items="items"
            class="elevation-1"
          >
            <template slot="headerCell" slot-scope="props">
              <v-tooltip bottom>
                <span slot="activator">
                  {{ props.header.text }}
                </span>
                <span>
                  {{ props.header.text }}
                </span>
              </v-tooltip>
            </template>
            <template slot="items" slot-scope="props">
              <td class="text-xs-center">{{ props.item.descripcion }}</td>
              <td class="text-xs-center">{{ props.item.precio_unidad }}</td>
              <td class="text-xs-center">{{ props.item.unidad }}</td>
              <td class="text-xs-center">{{ props.item.descuento1 }}</td>
              <td class="text-xs-center">{{ props.item.iva }}</td>
              <td class="text-xs-center">{{ props.item.transaccion }}</td>
            </template>
          </v-data-table>

          <div class="text-xs-center pt-2">
            <v-btn color="primary" @click="generardoc()" >
              <v-icon>fa-file</v-icon>
                Generar Documento
            </v-btn>
          </div>

        </v-card> 
        <!-- DATATABLE ITEMS NO ENCONTRADOS -->
        <v-card v-else >
          <v-card-title class="justify-center">
            <span class="secondary--text text-xs-center" style="font-size:200%;">Items no encontrados</span><br>
          </v-card-title>
          <v-data-table
            :headers="headersne"
            :items="itemsne"
            class="elevation-1"
          >
            <template slot="headerCell" slot-scope="props">
              <v-tooltip bottom>
                <span slot="activator">
                  {{ props.header.text }}
                </span>
                <span>
                  {{ props.header.text }}
                </span>
              </v-tooltip>
            </template>
            <template slot="items" slot-scope="props">
              <td class="text-xs-center">{{ props.item.descripcion }}</td>
              <td class="text-xs-center">{{ props.item.cod_barras }}</td>
              <td class="text-xs-center">{{ props.item.refcopi }}</td>
              <td class="text-xs-center">{{ props.item.costo_full }}</td>
              <td class="text-xs-center">{{ props.item.unidad }}</td>
              <td class="text-xs-center">{{ props.item.descuento }}</td>
              <td class="text-xs-center">{{ props.item.iva }}</td>
            </template>
          </v-data-table>
        </v-card> 
      </v-flex>
    </v-layout>

  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from "vue-property-decorator";
import Home from "./Home.vue";

@Component
export default class Factura extends Home {
  /*===========================================================================================================
                                          ATRIBUTOS
  =============================================================================================================*/
  private mostrarfac: boolean=false;
  private ent = [
    {
      id: "dia",
      titulo: "Dia",
      dato: "",
      tipo: "fecha",
      menu: null,
      validacion: "required"
    },
    {
      id: "fact",
      titulo: "Numero de Factura",
      dato: "",
      tipo: "select",
      // items: ["009VE", "015VE", "017VE", "020VE"],
      items: [],
      validacion: "required"
    },
    // {
    //   id: "nombre",
    //   titulo: "Nombre",
    //   dato: "",
    //   tipo: "texto",
    //   validacion: "required"
    // },
    // {
    //   id: "codcompra",
    //   titulo: "codigo comprador",
    //   dato: "",
    //   tipo: "numero",
    //   validacion: "required|max:4"
    // }
  ];

  /*===========================================================================================================
                                          METODOS
  =============================================================================================================*/
  constructor() {
    super();
  }

  private setfecha():void{
    if (this.ent[0].dato){
      // console.log(this.ent[0].dato);
      this.mostrarfac=true;

      const path = this.path+"facturas";
      this.axios
        .get(path, {
          params: {
            fecha: this.ent[0].dato
          }
        })
        .then(res => {
          this.ent[1].items = res.data.map(function(
          value: any,
          index: number
          ) {
            return value[0];
          });
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  }

  private getitems():void{
    const path = this.path+"items";
      this.axios
        .get(path, {
          params: {
            factura: this.ent[1].dato
          }
        })
        .then(res => {
          if (res.data){
            this.items = res.data.contenido.items;
            this.itemsne = res.data.contenido.itemsne;
            this.factura = res.data.contenido.factura;
            this.mostrart = true;
          }
        })
        .catch(error => {
          // eslint-disable-next-line
          console.error(error);
        });
  }
}
</script>