<template>
    <div class="cart_item">
        <div class="cart_column column_1">
            <el-checkbox class="my_el_checkbox" v-model="select"></el-checkbox>
        </div>
        <div class="cart_column column_2">
            <img :src="course.course_img" alt="">
            <span><router-link to="/course/detail/1">{{ course.name }}</router-link></span>
        </div>
        <div class="cart_column column_3">
            <el-select v-model="expire_id" size="mini" placeholder="请选择购买有效期" class="my_el_select">
                <el-option v-for="expire_time in course.expire_time" :label="expire_time.expire_text" :value="expire_time.id" :key="expire_time.id"></el-option>
            </el-select>
        </div>
        <div class="cart_column column_4">现价：¥{{ expire_price }}</div>
        <div class="cart_column column_4" @click="del_course">删除</div>
    </div>
</template>

<script>
export default {
    name: "CartItem",
    data() {
        return {
            expire: '永久有效',
            select: this.course.selected,
            expire_id: this.course.expire_id,
            expire_price: this.course.price,
            total_price: 0,
        }
    },
    methods: {
        // 实现删除课程的功能
        del_course() {
            let token = localStorage.token || sessionStorage.token
            console.log(this.course.id);
            this.$axios({
                url: this.$settings.HOST + 'cart/option/',
                method: "delete",
                data: {
                    course_id: this.course.id
                },
                headers: {
                    "Authorization": "jwt " + token
                }
            }).then(res => {
                console.log(res.data);
                this.$message({
                    message: res.data.message,
                    type: "success",
                    duration: 1000,
                })
                this.$emit('get_total')
                this.$emit('del', this.course)
                this.$store.commit('del_course', res.data.cart_length)
            }).catch(error => {
                console.log(error);
            })
        },

        // 勾选状态
        change_selected(){
            let token = localStorage.token || sessionStorage.token
            this.$axios({
                url: this.$settings.HOST+'cart/selected/',
                method:"post",
                data:{
                    course_id: this.course.id,
                    selected: this.select,
                },
                headers: {
                    "Authorization": "jwt " + token
                }
            }).then(res=>{
                this.$message({
                    message: '修改成功',
                    type: "success",
                    duration: 500,
                })
                this.course.selected = this.select
                console.log(this.course);
                this.$emit('get_total',this.course)
            }).catch(error=>{
                console.log(error);
                this.$message({
                    message: '修改失败',
                    type: "error",
                    duration: 500,
                })
            })
        },

        // 有效期的选择
        change_expire(){
            let token = localStorage.token || sessionStorage.token
            this.$axios({
                url: this.$settings.HOST + 'cart/expire/',
                method:"post",
                data:{
                    course_id:this.course.id,
                    expire_id: this.expire_id
                },
                headers: {
                    "Authorization": "jwt " + token
                }
            }).then(res=>{
                this.$message({
                    message: '修改成功',
                    type: "success",
                    duration: 500
                })
                this.expire_price = res.data.price
                this.course.price = res.data.price
                this.$emit('get_total',this.course)
            }).catch(error=>{
                console.log(error);
            })
        },
    },
    watch: {
        select() {
            this.change_selected()
        },
        expire_id(){
            this.change_expire()
        }
    },
    props: ['course']
}
</script>

<style scoped>
.cart_item::after {
    content: "";
    display: block;
    clear: both;
}

.cart_column {
    float: left;
    height: 250px;
}

.cart_item .column_1 {
    width: 88px;
    position: relative;
}

.my_el_checkbox {
    position: absolute;
    left: 0;
    right: 0;
    bottom: 0;
    top: 0;
    margin: auto;
    width: 16px;
    height: 16px;
}

.cart_item .column_2 {
    padding: 67px 10px;
    width: 520px;
    height: 116px;
}

.cart_item .column_2 img {
    width: 175px;
    height: 115px;
    margin-right: 35px;
    vertical-align: middle;
}

.cart_item .column_3 {
    width: 197px;
    position: relative;
    padding-left: 10px;
}

.my_el_select {
    width: 117px;
    height: 28px;
    position: absolute;
    top: 0;
    bottom: 0;
    margin: auto;
}

.cart_item .column_4 {
    padding: 67px 10px;
    height: 116px;
    width: 142px;
    line-height: 116px;
}

</style>
