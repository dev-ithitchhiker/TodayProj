# My Next.js App

This is a Next.js application that showcases today's recommended exhibitions. The data is fetched from a Firestore database.

## Getting Started

### Prerequisites

- Node.js
- npm (Node Package Manager)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/your-repo-name.git
   cd my-next-app
   ```

2. Install the dependencies:
   ```sh
   npm install
   ```

3. Set up Firebase:
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/).
   - Replace the Firebase configuration in `firebase.js` with your own Firebase project credentials.

### Running the Application

1. Start the development server:
   ```sh
   npm run dev
   ```

2. Open your browser and navigate to `http://localhost:3000`.

### Project Structure

- `firebase.js`: Initializes Firebase and Firestore.
- `app/page.tsx`: Main page component that fetches and displays today's recommended exhibitions.

### Dependencies

- [Next.js](https://nextjs.org/)
- [Firebase](https://firebase.google.com/)
- [Tailwind CSS](https://tailwindcss.com/)

### License

This project is licensed under the MIT License.
