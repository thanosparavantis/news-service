"use client";

import Link from "next/link";
import {FontAwesomeIcon} from "@fortawesome/react-fontawesome";
import {faMap} from "@fortawesome/free-solid-svg-icons";
import {usePathname} from "next/navigation";
import Image from "next/image";
import logo from "../logo.png";

export default function AppNavbar() {
  const pathName = usePathname();

  return (
    <nav className="z-[500] fixed top-0 w-full shadow-lg flex items-center justify-center min-h-12 bg-app opacity-95">
      <div
        className="max-w-3xl container flex flex-wrap items-center justify-between font-semibold text-sm tracking-wide text-gray-100">
        <Link
          href="/"
            className="ml-3 md:ml-0 pr-2 flex items-center gap-1 rounded transition focus:ring-2"
        >
          <Image
            src={logo}
            alt=""
            width={32}
            height={32}
            quality={100}
          />
          <div>
            Paravantis News
          </div>
        </Link>
        <Link
          href="/"
          className={
            `mr-2 md:mr-0 px-4 py-1.5
             flex items-center justify-center gap-2
             rounded hover:shadow-inner hover:bg-app-dark
             transition focus:ring-2
             ${pathName === "/map" ? " shadow-inner bg-app-dark" : ""}`
          }>
          <FontAwesomeIcon icon={faMap} size="sm"/>
          Χάρτης
        </Link>
      </div>
    </nav>
  )
}