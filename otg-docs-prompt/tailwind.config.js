import { table } from 'console';

/** @type {import('tailwindcss').Config} */
export default {
  purge: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: false, // or 'media' or 'class'
  content: [],
  variants: {
    extend: {},
  },
  theme: {
    extend: {
      animation: {
        marquee: 'marquee 25s linear infinite',
        marquee2: 'marquee2 25s linear infinite',
      },
      keyframes: {
        marquee: {
          '0%': { transform: 'translateX(0%)' },
          '100%': { transform: 'translateX(-100%)' },
        },
        marquee2: {
          '0%': { transform: 'translateX(100%)' },
          '100%': { transform: 'translateX(0%)' },
        },
      },

      colors: {
        customDark: '#379B47',
        customLight: '#f2f2f2',
        custombodyLight: '#ffffff',
        customSildbox: '#F2F2F2',
        customSildboxred: "#de4640",
        customSystempromt: '#F9EAEA',
        red_jetts: '#E43A32',
        text_bg_color_message_response: '#F9EAEA',
        textColor: '#2B2B2BE5',
        CardColor: '#94E1A7',
        switchColor: '#AFACFF',
        cuttomCreate: '#94E1A7',
        createdocument:'#FFFFFF',
        createred: '#e79e9c',
        customTr: '#F2F2F2',
        customTr1: '#D6FADB',
        customeChat:'#F8F9F8',
        tableColor: '#D6FADB',
        custtomebgSildbox: '#F0ECE5',
        Cancel:'#FFB5B5',
        textboxCreate: '#D6FBDB',
        textCreate: '#27A246',
      },

      fontFamily: {
        joan: ['Joan', 'serif'],
        jeju: ['"Jeju Gothic"', 'sans-serif'],
        Prompt:  ['Prompt', 'sans-serif'],        
      },
    },
  },
  plugins: [],
}