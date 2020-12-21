<template>
    <div class="footer">
        <ul>
            <li v-for="(foot,index) in footer_list" :key="index" v-if="foot.is_site"><a :href="foot.link">{{foot.title}}</a></li>
        </ul>
    </div>
</template>

<script>
export default {
    name: "Footer",
    data(){
        return{
            footer_list: []
        }
    },
    methods:{
        get_nav() {
            this.$axios.get(this.$settings.HOST+'home/nav/').then(response => {
                for (let n = 0; n < response.data.length; n++) {
                    if (response.data[n].position === 2) {
                        this.footer_list.push(response.data[n])
                    }
                }
            })
        },
    },
    created() {
        this.get_nav()
    }
}
</script>

<style scoped>
.footer {
    width: 100%;
    height: 128px;
    background: #f7f7f7;
    color: #fff;
}

.footer ul {
    margin: 0 auto 16px;
    padding-top: 38px;
    width: 810px;
}

.footer ul li {
    float: left;
    width: 112px;
    margin: 0 10px;
    text-align: center;
    font-size: 18px;
    color: #f7f7f7;
}

.footer ul::after {
    content: "";
    display: block;
    clear: both;
}

.footer p {
    text-align: center;
    font-size: 12px;
}
</style>
