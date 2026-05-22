import archiver from "archiver";
import chalk from "chalk";
import { randomBytes } from "crypto";
import fs from "fs";
import glob from "glob-promise";
import { globifyGitIgnore } from "globify-gitignore";
import path from "path";
import mcPackage from "mc-package.json";
import { createDirectories, emptyDirectory } from "scripts/utils/file";
import { ForgeManager } from "scripts/utils/forge";
import { readMinecraftPackage } from "scripts/utils/mc-package";
import {
  clientReleaseIgnorePath,
  directories,
  minecraftDirPath,
  releaseDirPath,
  serverReleaseIgnorePath,
  sharedReleaseIgnorePath,
} from "./constants";

async function main() {
  // Ensure release directory exists
  createDirectories(releaseDirPath);

  // Delete any existing files
  emptyDirectory(releaseDirPath);

  let clientFileName = `SkyFactory 5 v${mcPackage.version}`;
  let serverFileName = `SkyFactory 5 Server v${mcPackage.version}`;
  if (process.env.NODE_ENV !== "production") {
    const appendedText = `-${new Date()
      .toISOString()
      .slice(0, 10)}-${randomBytes(8).toString("hex")}`;

    clientFileName += appendedText;
    serverFileName += appendedText;
  }

  const { clientIgnore, serverIgnore } = await loadIgnoreFiles();

  // Client
  await createZip(
    directories,
    path.join(releaseDirPath, `${clientFileName}.zip`),
    clientIgnore,
  );

  //  Server
  // In CI we can't authenticate against Mojang to download the Forge installer.
  // Set SF5_CI_SKIP_FORGE_DOWNLOAD=true to build the server zip without the installer;
  // a SERVER_README.txt is added telling the operator which Forge build to fetch.
  const skipForgeDownload =
    process.env.SF5_CI_SKIP_FORGE_DOWNLOAD === "true";

  const additionalServerPaths: {
    isFile?: boolean;
    basePath: string;
    zipFilePath: (filePath: string) => string;
  }[] = [
    {
      basePath: path.join(process.cwd(), "src", "server"),
      zipFilePath: (filePath) => path.basename(filePath),
    },
  ];

  if (!skipForgeDownload) {
    const forgeManager = new ForgeManager(
      await readMinecraftPackage(),
      minecraftDirPath,
    );
    const minecraftInstallerFilePath = await forgeManager.ensureDownloaded();
    additionalServerPaths.unshift({
      isFile: true,
      basePath: path.relative(process.cwd(), minecraftInstallerFilePath),
      zipFilePath: (filePath) => path.basename(filePath),
    });
  } else {
    const mcPkg = await readMinecraftPackage();
    const readmePath = path.join(releaseDirPath, "SERVER_README.txt");
    const installerName = `forge-${mcPkg.minecraftVersion}-${mcPkg.forgeVersion}-installer.jar`;
    const installerUrl = `https://maven.minecraftforge.net/net/minecraftforge/forge/${mcPkg.minecraftVersion}-${mcPkg.forgeVersion}/${installerName}`;
    fs.writeFileSync(
      readmePath,
      [
        `SkyFactory 5 Server v${mcPackage.version}`,
        "",
        "This server zip was built in CI without bundling the Forge installer.",
        `Download the installer manually from:`,
        `  ${installerUrl}`,
        "",
        "Then run:",
        `  java -jar ${installerName} --installServer`,
        "",
        "and start the server with the included settings.sh / settings.bat.",
        "",
      ].join("\n"),
      "utf-8",
    );
    additionalServerPaths.unshift({
      isFile: true,
      basePath: path.relative(process.cwd(), readmePath),
      zipFilePath: (filePath) => path.basename(filePath),
    });
    console.log(
      chalk.yellow(
        `[CI] SF5_CI_SKIP_FORGE_DOWNLOAD=true — embedding SERVER_README.txt instead of forge installer`,
      ),
    );
  }

  await createZip(
    directories,
    path.join(releaseDirPath, `${serverFileName}.zip`),
    serverIgnore,
    additionalServerPaths,
  );
}

interface SourceFilePath {
  zipPath: string;
  cwdRelativePath: string;
}

async function createZip(
  sources: Map<string, string>,
  target: string,
  denylist: string[] = [],
  additionalPaths: {
    isFile?: boolean;
    basePath: string;
    zipFilePath: (filePath: string) => string;
  }[] = [],
): Promise<void> {
  const sourceFiles = (
    await Promise.all(
      Array.from(sources).map(async ([dir, rootPath]) => {
        const source = path
          .relative(process.cwd(), path.join(rootPath, dir))
          .replace(/\\/g, "/");

        const result = await glob(`${source}/**/*`, {
          cwd: process.cwd(),
          ignore: denylist,
          nocase: true,
        });

        const pattern = new RegExp(
          `^${path.relative(process.cwd(), source).replace(/\\/g, "/")}`,
        );

        return result.map<SourceFilePath>((file) => ({
          zipPath: file.replace(pattern, dir),
          cwdRelativePath: file,
          zipBasePath: dir,
        }));
      }),
    )
  ).flat();

  const additionalResolvedPaths = (
    await Promise.all(
      additionalPaths.map(async (additionalEntry) => {
        const basePath = additionalEntry.basePath.replace(/\\/g, "/");

        if (additionalEntry.isFile) {
          return {
            zipPath: additionalEntry.zipFilePath(basePath),
            cwdRelativePath: basePath,
          };
        }

        const result = await glob(
          `${path.relative(process.cwd(), basePath)}/**/*`,
          {
            cwd: process.cwd(),
            ignore: denylist,
            nocase: true,
          },
        );

        return result.map<SourceFilePath>((file) => ({
          zipPath: additionalEntry.zipFilePath(file),
          cwdRelativePath: file,
          zipBasePath: basePath,
        }));
      }),
    )
  ).flat();

  sourceFiles.push(...additionalResolvedPaths);

  return new Promise((resolve, reject) => {
    const output = fs.createWriteStream(target);
    const archive = archiver("zip", {
      zlib: { level: 9 },
    });

    output.on("close", () => {
      console.log(chalk.green(`Successfully created zip: ${target}`));
      resolve();
    });

    archive.on("error", (err: unknown) => {
      console.log(chalk.red(`An error occurred while creating zip: ${target}`));
      reject(err);
    });

    archive.pipe(output);

    sourceFiles.forEach((file) => {
      archive.file(path.join(process.cwd(), file.cwdRelativePath), {
        name: file.zipPath,
      });
    });

    archive.finalize();
  });
}

async function loadIgnoreFiles(): Promise<{
  clientIgnore: string[];
  serverIgnore: string[];
}> {
  const clientIgnoreData = fs.readFileSync(clientReleaseIgnorePath, "utf-8");
  const serverIgnoreData = fs.readFileSync(serverReleaseIgnorePath, "utf-8");
  const sharedIgnoreData = fs.readFileSync(sharedReleaseIgnorePath, "utf-8");

  return {
    clientIgnore: (
      await globifyGitIgnore(
        sharedIgnoreData + "\n" + clientIgnoreData,
        process.cwd(),
      )
    ).map((entry) => entry.glob),
    serverIgnore: (
      await globifyGitIgnore(
        sharedIgnoreData + "\n" + serverIgnoreData,
        process.cwd(),
      )
    ).map((entry) => entry.glob),
  };
}

main();
