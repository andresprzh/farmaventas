<template>
  <v-container grid-list-md>
    
    <h1 class="font-weight-black font-italic text-xs-center" >Formulario</h1>
    <!-- INPUTS FORMULARIO -->
      
    <v-form ref="form"  :v-model="valid" >
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
              v-validate="'required'"
              :data-vv-name=card.id
              @input="validar()"
            ></v-text-field>
            <!-- <v-date-picker :value="card.dato" v-model="card.dato" @input="card.menu = false" no-title autosave>
							</v-date-picker> -->
            <v-date-picker
              v-model="card.dato"
              no-title
              scrollable
            >
              <v-spacer></v-spacer>
              <v-btn flat color="primary" @click="validar();card.menu = false">Cancel</v-btn>
              <!-- <v-btn flat color="primary" @click="validar();$refs.menu[index].save(card.dato)">OK</v-btn> -->
              <v-btn flat color="primary" @click="fecha($refs.menu[index],card.dato)">OK</v-btn>
              <!-- <v-btn flat color="primary" @click="foo(index,card.dato)">OK</v-btn> -->
            </v-date-picker>
          </v-menu>

          <v-select v-else-if="card.tipo==='select'"
            ref="menu"
            v-validate="'required'"
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
          v-validate="'required'"
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
             />
            <label for="file">
              <v-icon style="color:white;">fa-upload</v-icon>
                Subir archivo
            </label>
        </v-flex>
      </v-layout>
      
      <v-layout row wrap>
        <v-flex xs12 md2 v-show="true" >
          <v-btn round
            color="primary"
            type="file"
            title="Cargar Acrhivo"
            :disabled="!valid"
            @click="submit"
          >Cargar 
          </v-btn>
        </v-flex>
      </v-layout>
    </v-form> 


    <v-layout row wrap>
      <v-flex xs12 v-show="mostrart" >
        <template>
          <v-data-table
            :headers="headers"
            :items="desserts"
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
              <td>{{ props.item.name }}</td>
              <td class="text-xs-right">{{ props.item.calories }}</td>
              <td class="text-xs-right">{{ props.item.fat }}</td>
              <td class="text-xs-right">{{ props.item.carbs }}</td>
              <td class="text-xs-right">{{ props.item.protein }}</td>
              <td class="text-xs-right">{{ props.item.iron }}</td>
            </template>
          </v-data-table>
        </template>
      </v-flex>
    </v-layout>

  </v-container>
</template>

<script lang="ts">
import { Component, Vue } from 'vue-property-decorator';

@Component
export default class Home extends Vue {

  private file: any;
  private mostrart: boolean = false;
  // private Item: string = '';
  private valid = true;
  // private entradas: object [];
  private entradas = [
    { id: 'dia', titulo: 'Dia', dato: '', tipo: 'fecha', menu: null },
    // { id: 'drog', titulo: 'Codigo Drogueria', dato: '', tipo: 'numero' },
    { id: 'drog', titulo: 'Codigo Drogueria', dato: '', tipo: 'select', items: ['sede1', 'sede2', 'sede3'] },
    { id: 'nombre', titulo: 'Nombre', dato: '', tipo: 'texto' },
    { id: 'codcompra', titulo: 'codigo compra', dato: '', tipo: 'numero' },
    { id: 'ftramite', titulo: 'Fecha tramite', dato: '', tipo: 'fecha', menu: null },
  ];

  private headers = [
          {
            text: 'Dessert (100g serving)',
            align: 'left',
            sortable: false,
            value: 'name',
          },
          { text: 'Calories', value: 'calories' },
          { text: 'Fat (g)', value: 'fat' },
          { text: 'Carbs (g)', value: 'carbs' },
          { text: 'Protein (g)', value: 'protein' },
          { text: 'Iron (%)', value: 'iron' },
  ];

  private desserts = [
          {
            value: false,
            name: 'Frozen Yogurt',
            calories: 159,
            fat: 6.0,
            carbs: 24,
            protein: 4.0,
            iron: '1%',
          },
          {
            value: false,
            name: 'Ice cream sandwich',
            calories: 237,
            fat: 9.0,
            carbs: 37,
            protein: 4.3,
            iron: '1%',
          },
          {
            value: false,
            name: 'Eclair',
            calories: 262,
            fat: 16.0,
            carbs: 23,
            protein: 6.0,
            iron: '7%',
          },
          {
            value: false,
            name: 'Cupcake',
            calories: 305,
            fat: 3.7,
            carbs: 67,
            protein: 4.3,
            iron: '8%',
          },
          {
            value: false,
            name: 'Gingerbread',
            calories: 356,
            fat: 16.0,
            carbs: 49,
            protein: 3.9,
            iron: '16%',
          },
          {
            value: false,
            name: 'Jelly bean',
            calories: 375,
            fat: 0.0,
            carbs: 94,
            protein: 0.0,
            iron: '0%',
          },
          {
            value: false,
            name: 'Lollipop',
            calories: 392,
            fat: 0.2,
            carbs: 98,
            protein: 0,
            iron: '2%',
          },
          {
            value: false,
            name: 'Honeycomb',
            calories: 408,
            fat: 3.2,
            carbs: 87,
            protein: 6.5,
            iron: '45%',
          },
          {
            value: false,
            name: 'Donut',
            calories: 452,
            fat: 25.0,
            carbs: 51,
            protein: 4.9,
            iron: '22%',
          },
          {
            value: false,
            name: 'KitKat',
            calories: 518,
            fat: 26.0,
            carbs: 65,
            protein: 7,
            iron: '6%',
          },
  ];
  // Mensajes custom error vee validate
  private dictionary = {
    custom: {
      dia: {
        required: () => 'Por favor seleccione un dia ',
        // custom messages
      },
      drog: {
        required: 'Por favor seleccione una sede',
      },
      nombre: {
        required: 'Por favor digite el nombre',
      },
      codcompra: {
        required: 'por favor digite el codigo de compra',
      },
      ftramite: {
        required: 'Por favor seleccione una fecha',
      },
    },
  };

  constructor() {
    super();
  }

  private mounted() {
    this.$validator.localize('es', this.dictionary);
  }

  private processFile(event: any) {
    this.$validator.validateAll().then((result) => {
      if (result) {
        this.file = event.target.files[0];
        // const valid: boolean = true;
        if (this.valid) {
          // alert('hola');
          this.mostrart = true;
        }
        // console.log(this.file);
      }
    });
  }
  private submit(): void {
    this.$validator.validateAll().then((result) => {
      if (result) {
        alert('hola');
      }
    });
    const ent = this.entradas[0];
  }
  private fecha(ref: any,dato: string) :void {
    this.validar();
    ref.save(dato);
  }
  private validar(): void{
    this.$validator.validateAll().then((result) => {
      if (result) {        
        this.valid=true;
      }
    });
  }
}
</script>

<style scoped>
  input[type=file] {
    width: 0.1px;
    height: 0.1px;
    opacity: 0;
    overflow: hidden;
    position: absolute;
    z-index: -1;
  }

  input[type=file] + label {
    /* font-size: 1.25em; */
    padding: 5px;
    border-radius: 20px;
    font-weight: 700;
    color: white;
    background-color: #1B5E20;
    display: inline-block;
    cursor: pointer;
  }

  input[type=file]:focus + label,
  input[type=file] + label:hover {
      background-color: rgb(57, 148, 63);
      outline: 1px dotted #000;
	    outline: -webkit-focus-ring-color auto 5px;
  }
</style>