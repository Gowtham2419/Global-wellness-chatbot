const express = require("express");
const mongoose = require("mongoose");
const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const cors = require("cors");
require("dotenv").config();

const app = express();
app.use(express.json());
app.use(cors());

// MongoDB Connection
mongoose.connect("mongodb://localhost:27017/auth_demo", {
    useNewUrlParser: true,
    useUnifiedTopology: true
}).then(() => console.log("MongoDB connected"))
  .catch(err => console.log(err));

// User Schema
const userSchema = new mongoose.Schema({
    name: String,
    email: { type: String, unique: true },
    password: String,
    ageGroup: String,
    language: { type: String, default: "English" }
});

const User = mongoose.model("User", userSchema);

// Register
app.post("/register", async (req, res) => {
    try {
        const { name, email, password, ageGroup, language } = req.body;
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = new User({ name, email, password: hashedPassword, ageGroup, language });
        await user.save();
        res.json({ message: "User registered successfully" });
    } catch (error) {
        res.status(400).json({ error: "User already exists" });
    }
});

// Login
app.post("/login", async (req, res) => {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    if (!user) return res.status(400).json({ error: "Invalid email" });

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return res.status(400).json({ error: "Invalid password" });

    const token = jwt.sign({ id: user._id }, process.env.JWT_SECRET, { expiresIn: "1h" });
    res.json({ token, user });
});

// Middleware for Auth
const authMiddleware = (req, res, next) => {
    const token = req.headers["authorization"];
    if (!token) return res.status(403).json({ error: "No token provided" });

    jwt.verify(token, process.env.JWT_SECRET, (err, decoded) => {
        if (err) return res.status(401).json({ error: "Invalid token" });
        req.userId = decoded.id;
        next();
    });
};

// Get Profile
app.get("/profile", authMiddleware, async (req, res) => {
    const user = await User.findById(req.userId).select("-password");
    res.json(user);
});

// Update Profile
app.put("/profile", authMiddleware, async (req, res) => {
    const { name, ageGroup, language } = req.body;
    const user = await User.findByIdAndUpdate(req.userId, { name, ageGroup, language }, { new: true });
    res.json(user);
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => console.log(`Server running on port ${PORT}`));
