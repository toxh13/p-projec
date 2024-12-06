const mongoose = require('mongoose');

const clothingSchema = new mongoose.Schema({
    name: { type: String, required: true },
    gender: { type: String, required: true },
    category: { type: String, required: true }, // 상의, 하의 등
    size: { type: String, required: true },
    color: { type: String, required: true },
    price: { type: Number, required: true }
});

module.exports = mongoose.model('Clothing', clothingSchema);
