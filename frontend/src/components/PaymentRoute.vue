<template>
    <ul class="route">
        <li>
            <span>10:03</span> 
            <div><strong>GBP 200</strong> 2d 12h 15m</div>
        </li>
        <li>
            <span>10:03</span> 
            <div><strong>GBP 200</strong> 2d 12h 15m</div>
        </li>
        <li>
            <span>10:03</span> 
            <div><strong>GBP 200</strong> 2d 12h 15m</div>
        </li>
        <li>
            <span>10:03</span> 
            <div><strong>GBP 200</strong> 2d 12h 15m</div>
        </li>
        <li>
            <span>10:03</span> 
            <div><strong>GBP 200</strong> 2d 12h 15m</div>
        </li>
        <li>
            <span>10:03</span> 
            <div><strong>GBP 200</strong> 2d 12h 15m</div>
        </li>
    </ul>
</template>

<style lang="scss" scoped>
    .route li { 
        display: flex; 
    }

    .route span { 
        position: relative;
        color: #ccc;
        padding: 0 1.5em;  
    }

    .route span::after { 
        content: "";
        position: absolute;
        z-index: 2;
        right: 0;
        top: 0;
        transform: translateX(50%);
        border-radius: 50%;
        background: #fff;
        border: 1px #ccc solid;
        width: .8em;
        height: .8em;
    }


    .route div {
        padding: 0 1.5em 6.5em 1.5em;
        position: relative;
        min-width: 200px;
        display: block;
    }

    .route div::before {
        content: "";
        position: absolute;
        z-index: 1;
        left: 0;
        height: 100%;
        border-left: 1px #ccc solid;
    }

    .route strong {
        display: block;
        font-weight: bolder;
    }

    .route { 
        margin: 1em;
        width: 100%;
        display: block;
        margin: auto;
        max-width: 300px;
    }
    .route, 
    .route *::before, 
    .route *::after { box-sizing: border-box; }
</style>