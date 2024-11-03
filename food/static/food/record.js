document.addEventListener('alpine:init', () => {
    Alpine.data('recordName', () => ({
        resize() {
            this.$el.style.fontSize = "";
            let fontSize = window.getComputedStyle(this.$el).getPropertyValue('font-size');
            fontSize = parseFloat(fontSize);
            // while (this.$el.scrollHeight > this.$el.clientHeight) {
            //     fontSize -= 0.1;
            //     this.$el.style.fontSize = `${fontSize}px`;
            // }
            while (this.$el.scrollWidth > this.$el.clientWidth) {
                fontSize -= 1;
                this.$el.style.fontSize = `${fontSize}px`;
            }
        },

        init() {
            this.resize();
        }
    }));
});