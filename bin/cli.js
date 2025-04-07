#!/usr/bin/env node

const { program } = require('commander');
const clear = require('clear');
const chalk = require('chalk');
const figlet = require('figlet');
const setupProcess = require('../src/index');
const pkg = require('../package.json');

// Clear the console
clear();

// Display welcome banner
console.log(
  chalk.yellow(
    figlet.textSync('Places API Setup', { horizontalLayout: 'full' })
  )
);
console.log(chalk.yellow(`v${pkg.version}\n`));

// Setup CLI commands
program
  .version(pkg.version)
  .description('Google Places API setup and registration tool')
  .option('-s, --skip-auth', 'Skip authentication (use existing gcloud auth)')
  .option('-p, --project-id <id>', 'Specify project ID')
  .option('-n, --project-name <n>', 'Specify project name')
  .option('-y, --yes', 'Auto-confirm all prompts (non-interactive mode)')
  .option('--no-billing', 'Skip billing setup (limited functionality)')
  .option('--mock-billing', 'Use mock billing mode for development only')
  .option('--debug', 'Enable debug mode with additional information')
  .action(async (options) => {
    try {
      if (options.debug) {
        console.log(chalk.blue('Running in debug mode'));
      }
      
      // Set the default --yes flag to true if not explicitly set
      if (options.yes === undefined) {
        options.yes = true;
      }
      
      const result = await setupProcess.run(options);
      
      if (!result.success) {
        if (result.error === 'Please restart terminal to use Google Cloud SDK.') {
          console.log(chalk.yellow('\nGoogle Cloud SDK was installed, but your PATH needs to be updated.'));
          console.log(chalk.yellow('Please restart your terminal and run this command again to continue setup.'));
          console.log(chalk.green('The installation is partially complete.'));
        } else {
          console.error(chalk.red('Error during setup:'), result.error);
        }
        process.exit(1);
      }
      
      // Successful completion
      if (result.apiKey) {
        console.log(chalk.green('\nAPI Key is ready for use:'), chalk.yellow(result.apiKey));
        console.log(chalk.yellow('\nRemember to restrict your API key as needed for production use.'));
        
        // Add note for alternative billing options if used
        if (options.noBilling || options.mockBilling) {
          console.log(chalk.yellow('\nNOTE: You\'re using a limited billing setup. Some API features may not work in production.'));
          console.log(chalk.yellow('For full functionality, enable billing through the Google Cloud Console.'));
        }
      }
      
    } catch (error) {
      console.error(chalk.red('Error during setup:'), error.message);
      process.exit(1);
    }
  });

program.parse(process.argv); 