<template>
  <div>
    <b-alert
      variant="danger"
      v-model="hasError"
      dismissible
      style="width: 40%; position: absolute; top: 0; left: 30%"
    >{{ error }}</b-alert>

    <el-steps :active="2" finish-status="success" align-center style="margin: 0 auto">
      <el-step title="Sign Up"></el-step>
      <el-step title="Verify Your Password"></el-step>
      <el-step title="Fill In Your Information"></el-step>
    </el-steps>
    <div id="userinfo">
      <h4 style="text-align: center; padding: 10px 0">Fill in your information</h4>

      <b-form @submit.prevent="onSubmit">
        <ul class="main">
          <li class="icon">
            <label for="icon">Choose an image as your icon</label>
            <img :src="icon" alt="User Icon" id="icon">
            <input
              id="choose"
              type="file"
              name="icon"
              accept="image/*"
              @change="changeImg($event)"
              ref="icon"
            >
          </li>

          <li class="name">
            <b-form-group class="fullname" label="Name" label-for="firstname" horizontal>
              <b-row>
                <b-col cols="6">
                  <b-form-input
                    id="firstname"
                    type="text"
                    v-model="firstname"
                    placeholder="firstname"
                    required
                  />
                </b-col>
                <b-col cols="6">
                  <b-form-input
                    id="secondname"
                    type="text"
                    v-model="secondname"
                    placeholder="secondname"
                    required
                  />
                </b-col>
              </b-row>
            </b-form-group>
          </li>

          <li class="biography">
            <label for="biography">Biography</label>
            <b-form-input id="biography" type="text" v-model="biography"/>
          </li>

          <li class="company">
            <label for="company">Company</label>
            <b-form-input id="company" type="text" v-model="company"/>
          </li>

          <li class="location">
            <label for="location">Location</label>
            <b-form-input id="location" type="text" v-model="location"/>
          </li>

          <li class="website">
            <label for="website">Website</label>
            <b-form-input id="website" type="text" v-model="website"/>
          </li>

          <li class="operation">
            <b-button type="submit" variant="primary" class="submit">Submit</b-button>
          </li>
        </ul>
      </b-form>
    </div>
  </div>
</template>

<script>
// window.onload = function() {
//   let img = document.getElementById('icon');
//   let input = document.getElementById('choose');
//   img.onclick = function() {
//     input.click();
//   }
// }
import globals from "@/globals";
import axios from "axios";
export default {
  name: "SignupFinishing",
  data() {
    return {
      icon: require("../images/choose_icon.jpg"),
      firstname: "",
      secondname: "",
      biography: "",
      company: "",
      location: "",
      website: "",
      error: "",
      hasError: false
    };
  },
  created() {
    if (
      globals.cache.password == undefined ||
      globals.cache.username == undefined ||
      globals.cache.token == undefined
    ) {
      window.location.replace("/");
    }
  },
  methods: {
    changeImg(e) {
      let file = e.target.files[0];
      let reader = new FileReader();
      let that = this;
      if (file.size < 200 * 1024) {
        reader.readAsDataURL(file);
        reader.onload = function() {
          that.icon = this.result;
        };
      } else {
        e.target.value = "";
        alert("file size exceed limit, the max size 200KB");
      }
    },
    onSubmit(e) {
      e.preventDefault();
      let password = globals.cache.password;
      let username = globals.cache.username;
      let token = globals.cache.token;
      let icon;
      let tmp = this.icon.match(/data:image\/jpeg;base64,(.*)/);
      if (tmp == null) {
        icon = null;
      } else {
        icon = tmp[1];
      }
      axios({
        method: "POST",
        url: "/signup/finishing",
        data: {
          username: username,
          password: password,
          token: token,
          icon: icon,
          firstname: this.firstname,
          secondname: this.secondname,
          biography: this.biography,
          company: this.company,
          location: this.location,
          website: this.website
        }
      }).then(response => {
        if (response.data.state == "ok") {
          globals.cache.password = null;
          this.$router.replace("/signin");
        } else {
          this.error = response.data.error;
          this.hasError = true;
        }
      });
    }
  }
};
</script>

<style scoped>
#userinfo {
  width: 640px;
  height: 100%;
  margin: 0 auto;
  margin-top: 10px;
}
ul {
  list-style: none;
  margin-top: 1rem;
  border: 1px solid #d7dee2;
}
ul li {
  list-style: none;
  width: 100%;
  margin-left: -20px;
  padding: 0.6rem 0;
}
.icon > img {
  display: block;
  width: 100px;
  height: 100px;
  background-size: 100%;
}
/* .icon > input {
  display: none;
} */
</style>

<style>
#userinfo .name .fullname label:after {
  content: " *";
  color: red;
}
</style>
