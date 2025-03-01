export default function handler(req, res) {
    try {
        res.status(200).json({ message: "API 정상 동작!" });
    } catch (error) {
        res.status(500).json({ error: "Internal Server Error" });
    }
}