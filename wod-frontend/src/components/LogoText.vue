<template>
    <h1 class="knockout">
        Build My Waifu
    </h1>
</template>
<style>
    .knockout {
        text-align: center;
        font-family: Comic Sans MS, Comic Sans, cursive;
        font-size: 3rem;
        background: linear-gradient(110deg, #efdc0a 33%, rgba(0, 0, 0, 0) 33%), linear-gradient(110deg, #ffffff 34%, #cf7ccd 34%);
        background-size: 400%;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        animation: Gradient 5s ease infinite;
        -webkit-animation: Gradient 15s ease infinite;
        -moz-animation: Gradient 5s ease infinite;
    }

    @keyframes Gradient {
        0% {
            background-position: 32% 50%
        }

        50% {
            background-position: 25.5% 50%
        }

        100% {
            background-position: 32% 50%
        }
    }
</style>