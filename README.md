<!DOCTYPE html>
<html>
<head>
  <title>Starlink Beam Planner</title>
  <style>
      body {
          font-family: Helvetica, sans-serif;
      }
  
      @media (min-width: 750px) {
          body {
              width: 750px;
              margin: 0 auto;
          }
      }

      table {
          margin: auto;
      }

      table th, table td {
          padding-left: 1em;
      }
  </style>
</head>
<body>



<h1>Starlink Beam Planner</h1>

<p>To provide internet to a user, a satellite forms a "beam" towards that user and the user forms a beam towards the satellite. After doing this the satellite and user can form a high-bandwidth wireless link.</p>

<p>Starlink satellites are designed to be very flexible. For this problem, each satellite is capable of forming up to 32 independent beams simultaneously. Therefore one Satellite can serve up to 32 users. Each beam is assigned one of 4 "colors" corresponding to the frequencies used to communicate with that user.</p>

<p>There are a few constraints on how those beams can be placed:</p>

<ul>
    <li>From the user's perspective, the beam serving them must be within 45 degrees of vertical. Assume a spherical Earth, such that all surface normals pass through the center of the Earth (0, 0, 0).</li>
    <li>On each Starlink satellite, no two beams of the same color may be pointed within 10 degrees of each other, or they will interfere with one another.</li>
</ul>

<div style="text-align: center"><img src="resources/diagram.svg" /></div>



<h2>Optimization Problem</h2>

<p>Given a list of users and satellites, assign beams to users respecting the constraints above. Some test cases have more users than can be physically served.</p>

<p>The solution will be run on a number of test cases. Each case includes a minimum number of users that <b>must</b> be served. Constraint violations, crashes, unhandled exceptions, serving less than the minimum number of users, or taking longer than <b>60 seconds</b> will all result in failure. </p>
<p>Optimize user coverage given constraints in the shortest amount of time. </p>

<table>
    <tr><th></th><th>Users</th><th>Satellites</th><th>Min Coverage</th></tr>
    <tr><th>Case 1</th><td>2</td><td>1</td><td>100%</td></tr>
    <tr><th>Case 2</th><td>5</td><td>1</td><td>80%</td></tr>
    <tr><th>Case 3</th><td>1000</td><td>64</td><td>95%</td></tr>
    <tr><th>Case 4</th><td>5000</td><td>700</td><td>80%</td></tr>
    <tr><th>Case 5</th><td>50000</td><td>36</td><td>1%</td></tr>
    <tr><th>Case 6</th><td>10000</td><td>720</td><td>80%</td></tr>
</table>

<h2>Usage</h2>

<p>Solution implemented in Python in <code>solution.py</code>. Only Python standard library and anything provided in <code>util.py</code> was used, no other third party libraries.</p>

<p>Run <code>make</code> within the <code>/py</code> folder to run all tests.</p>

<p>Test results will be printed to the console. This includes user coverage and runtime as well as failure to satisfy constraints.</p>

<div style="text-align: left"><img src="resources/output.png" style="width: 75%"/></div>

</body>
</html>
