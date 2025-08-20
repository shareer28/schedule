# Metric Data Uploader Front-End

## Developing the Application with Vite

This project uses [Vite](https://vitejs.dev/) as its build tool and development server. Vite provides fast startup, hot module replacement, and an optimized build process for modern web applications.

### Prerequisites

- [Node.js](https://nodejs.org/) (v16 or higher recommended)
- [Yarn](https://yarnpkg.com/) or [npm](https://www.npmjs.com/)

### Install Dependencies

Install all required dependencies using your preferred package manager:

```bash
yarn install
# or
npm install
```

### Start the Development Server

To start the Vite development server with hot module replacement:

```bash
yarn dev
# or
npm run dev
```

The app will be available at [http://localhost:5173](http://localhost:5173) by default.

### Project Structure

- `src/` — Main source code (components, pages, hooks, utils, etc.)
- `public/` — Static assets
- `vite.config.ts` — Vite configuration

### Build for Production

To create an optimized production build:

```bash
yarn build
# or
npm run build
```

The output will be in the `dist/` directory.

### Additional Tips

- Vite supports [Hot Module Replacement (HMR)](https://vitejs.dev/guide/features.html#hot-module-replacement) for fast feedback during development.
- You can customize Vite's behavior in `vite.config.ts`.
- For more information, see the [Vite documentation](https://vitejs.dev/).
