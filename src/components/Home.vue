<template>
  <v-container grid-list-md>
    
    <h1 class="font-weight-black font-italic text-xs-center" >Titulo</h1>
    <!-- INPUTS FORMULARIO -->
      
    <v-form ref="form"  :v-model="valid" v-show="!mostrart" >
      <v-layout row wrap>
        <v-flex 
        xs12
        v-for="(card,index) in entradas"
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
              
              <v-btn flat color="primary" @click="fecha($refs.menu[index],card.dato)">OK</v-btn>
              
            </v-date-picker>
          </v-menu>

          <v-select v-else-if="card.tipo==='select'"
            ref="menu"
            v-validate="card.validacion"
            :items="card.items"
            v-model="card.dato"
            :error-messages="errors.collect(card.id)"
            label="Sede"
            :data-vv-name=card.id
            @change="validar()"
            required
          ></v-select>
          <v-text-field v-else
          ref="menu"
          v-model="card.dato"
          v-validate="card.validacion"
          :error-messages="errors.collect(card.id)"
          :label=card.titulo
          :data-vv-name=card.id 
          required
          @change="validar()"
          ></v-text-field>
        </v-flex>
      </v-layout>

      <v-layout row wrap>
        <v-flex xs12 md2 v-show=true >
             <input 
             type="file" name="file" id="file"
             :disabled="!valid"
             @change="processFile($event)"
             @click="inputclick($event)"
             />
             
            <label for="file">
              <v-icon style="color:white;">fa-upload</v-icon>
               {{filename}}
            </label>
            
        </v-flex>
      </v-layout>
      
      <!-- <v-layout row wrap>
        <v-flex xs12 md2 v-show="true" >
          <v-btn round
            color="primary"
            title="Cargar Acrhivo"
            :disabled="!valid"
            @click="submit()"
          >Cargar 
          </v-btn>
        </v-flex>
      </v-layout> -->

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
            <span class="secondary--text text-xs-center" style="font-size:200%;">Items encontrados</span><br>
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
            <v-btn color="primary" >
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

@Component
export default class Home extends Vue {
  /*===========================================================================================================
                                          ATRIBUTOS
  =============================================================================================================*/
  private file: any = {};
  private tabla: string = "";
  private mostrart: boolean = false;
  // private Item: string = '';
  private filename: string = "Subir archivo";
  private valid = true;
  private items: object[] = [];
  private itemsne: object[] = [];
  // private entradas: object [];
  private entradas = [
    {
      id: "dia",
      titulo: "Dia",
      dato: "",
      tipo: "fecha",
      menu: null,
      validacion: "required"
    },
    {
      id: "drog",
      titulo: "Codigo Drogueria",
      dato: "",
      tipo: "select",
      // items: ["009VE", "015VE", "017VE", "020VE"],
      items: [],
      validacion: "required"
    },
    {
      id: "nombre",
      titulo: "Nombre",
      dato: "",
      tipo: "texto",
      validacion: "required"
    },
    {
      id: "codcompra",
      titulo: "codigo comprador",
      dato: "",
      tipo: "numero",
      validacion: "required|max:4"
    }
  ];

  private headers = [
    { text: "Descripcion", align: "left", value: "desc" },
    { text: "Precio unidad", value: "precio" },
    { text: "Unidad", value: "unidad" },
    { text: "Descuento", value: "des" },
    { text: "Iva", value: "iva" },
    { text: "Transaccion", value: "tran" }
  ];

  private headersne = [
    { text: "Descripcion", align: "left", value: "desc" },
    { text: "Codigo de barras", value: "codbar" },
    { text: "Referencia", value: "referencia" },
    { text: "Precio unidad", value: "fecha" },
    { text: "Unidad", value: "factura" },
    { text: "Descuento", value: "ref" },
    { text: "Iva", value: "descripcion" }
  ];

  // Mensajes custom error vee validate
  private dictionary = {
    custom: {
      dia: {
        required: () => "Por favor seleccione un dia "
        // custom messages
      },
      drog: {
        required: "Por favor seleccione una sede"
      },
      nombre: {
        required: "Por favor digite el nombre"
      },
      codcompra: {
        required: "por favor digite el codigo de compra",
        max: "Maximo 4 caracteres"
      },
      ftramite: {
        required: "Por favor seleccione una fecha"
      },
      nit: {
        required: "Por favor digite el NIT"
      }
    }
  };

  /*===========================================================================================================
                                          METODOS
  =============================================================================================================*/
  constructor() {
    super();

    const path = "http://localhost:5000/puntosv";
    this.axios
      .get(path, {
        params: {
          dato: "all"
        }
      })
      .then(res => {
        this.entradas[1].items = res.data.map(function(
          value: any,
          index: number
        ) {
          return value["num_sede"];
        });
      })
      .catch(error => {
        // eslint-disable-next-line
        console.error(error);
      });
  }

  private mounted() {
    this.$validator.localize("es", this.dictionary);
  }

  private processFile(event: any) {
    this.$validator.validateAll().then(result => {
      if (result) {
        this.file = event.target.files[0];
        this.filename = this.file.name;
        let formData = new FormData();
        formData.append("file", this.file);
        formData.append("fecha", this.entradas[0].dato);
        formData.append("sede", this.entradas[1].dato);
        formData.append("nombre", this.entradas[2].dato);
        formData.append("codigocom", this.entradas[3].dato);
        // const valid: boolean = true;
        const path = "http://localhost:5000/copiupload";

        this.axios
          .post(path, formData, {
            headers: { "Content-Type": "multipart/form-data" }
          })
          .then(res => {
            // this.msg = res.data;
            console.log(res.data);
            if (res.data) {
              this.items = res.data.items;
              this.itemsne = res.data.itemsne;
              this.mostrart = true;
            } else {
              alert("error al subir el arcivo");
            }
          })
          .catch(error => {
            // eslint-disable-next-linen
            console.error(error);
          });
      }
    });
  }

  private inputclick(event: any) {
    this.$validator.validateAll().then(result => {
      if (!result) {
        event.preventDefault();
      }
    });
  }

  // private submit(): void {
  //   this.$validator.validateAll().then(result => {
  //     if (result) {
  //       const path = "http://localhost:5000/ping";
  //       this.axios
  //         .get(path, {
  //           params: {
  //             dato: "asdñdlakdlak"
  //           }
  //         })
  //         .then(res => {
  //           // this.msg = res.data;
  //           alert(res.data);
  //         })
  //         .catch(error => {
  //           // eslint-disable-next-line
  //           console.error(error);
  //         });
  //     }
  //   });
  // }

  private fecha(ref: any, dato: string): void {
    this.validar();
    ref.save(dato);
  }

  private validar(): void {
    this.$validator.validateAll().then(result => {
      if (result) {
        this.valid = true;
      }
    });
  }
}
</script>

<style scoped>
input[type="file"] {
  width: 0.1px;
  height: 0.1px;
  opacity: 0;
  overflow: hidden;
  position: absolute;
  z-index: -1;
}

input[type="file"] + label {
  padding: 5px;
  border-radius: 20px;
  font-weight: 700;
  color: white;
  background-color: #1b5e20;
  display: inline-block;
  cursor: pointer;
}

input[type="file"]:focus + label,
input[type="file"] + label:hover {
  background-color: rgb(57, 148, 63);
  outline: 1px dotted #000;
  outline: -webkit-focus-ring-color auto 5px;
}
</style>